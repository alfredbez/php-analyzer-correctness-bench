"""Case model and validation.

A case is a directory under ``cases/<domain>/<slug>/`` that a human can run by
hand. The contract is deliberately strict: an expectation without a stated basis
is rejected, because an ungrounded expectation turns a benchmark into an
opinion poll.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CASES_DIR = os.path.join(ROOT, "cases")

TOOLS = ("phpstan", "psalm", "mago")

# How the ground truth of a case is justified, weakest last.
BASES = (
    "php_semantics",        # the language or the runtime decides it
    "runtime_proof",        # the case ships a script whose exit code decides it
    "upstream_test",        # taken from the analyzer's own test suite expectations
    "upstream_docs",        # documented behaviour of the tool
    "maintainer_statement",  # a maintainer said so, with a link
)

# Verdict vocabulary. Kept small on purpose; the report aggregates on it.
MODES = ("diagnostics", "clean", "unsupported")

REQUIRED_CASE_KEYS = ("id", "title", "domain", "rule_class", "ground_truth", "expect")

_ID_RE = re.compile(r"^[a-z0-9]+(?:[a-z0-9-]*[a-z0-9])?/[a-z0-9]+(?:[a-z0-9-]*[a-z0-9])?$")


class CaseError(ValueError):
    pass


@dataclass
class Case:
    path: str
    data: dict
    diagnostics: list[str] = field(default_factory=list)

    # -- convenience accessors ------------------------------------------

    @property
    def id(self) -> str:
        return self.data["id"]

    @property
    def criterion_id(self) -> str:
        return self.data.get("criterion_id", self.id)

    @property
    def domain(self) -> str:
        return self.data["domain"]

    @property
    def rule_class(self) -> str:
        return self.data["rule_class"]

    @property
    def slug(self) -> str:
        return self.id.split("/", 1)[1]

    @property
    def target_dirs(self) -> list[str]:
        return self.data.get("targets", ["src"])

    @property
    def php_min(self) -> str:
        return self.data.get("php", {}).get("min", "8.1")

    @property
    def php_max(self) -> str | None:
        return self.data.get("php", {}).get("max")

    @property
    def phpstan_level(self) -> int:
        return int(self.data.get("config", {}).get("phpstan", {}).get("level", 9))

    @property
    def needs_composer_install(self) -> bool:
        return bool(self.data.get("composer", {}).get("install", False))

    @property
    def runtime_script(self) -> str | None:
        return self.data.get("ground_truth", {}).get("runtime_script")

    def expectation(self, tool: str) -> dict:
        return self.data["expect"].get(tool, {"mode": "unsupported",
                                              "reason": "no expectation recorded for this tool"})

    def abs_path(self, *parts: str) -> str:
        return os.path.join(self.path, *parts)


def _load_json(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def discover(cases_dir: str = CASES_DIR) -> list[Case]:
    cases = []
    for dirpath, dirnames, filenames in os.walk(cases_dir):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "__pycache__"]
        if "case.json" in filenames:
            cases.append(load(dirpath))
    cases.sort(key=lambda case: case.id)
    return cases


def load(case_dir: str) -> Case:
    manifest = os.path.join(case_dir, "case.json")
    data = _load_json(manifest)
    case = Case(path=case_dir, data=data)
    case.diagnostics = validate(case)
    return case


def validate(case: Case) -> list[str]:
    """Return a list of problems. Empty means the case satisfies the contract."""
    problems: list[str] = []
    data = case.data

    for key in REQUIRED_CASE_KEYS:
        if key not in data:
            problems.append(f"missing required key: {key}")

    case_id = data.get("id", "")
    if case_id and not _ID_RE.match(case_id):
        problems.append(f"id must look like '<domain>/<slug>', got {case_id!r}")
    if case_id and case.path.split(os.sep)[-2:] != case_id.split("/"):
        problems.append(f"id {case_id!r} does not match its directory {os.sep.join(case.path.split(os.sep)[-2:])!r}")

    if "criterion_id" in data:
        criterion = data["criterion_id"]
        if (not isinstance(criterion, str) or not _ID_RE.fullmatch(criterion)
                or criterion.split("/")[0] != data.get("domain")):
            problems.append("criterion_id must be '<domain>/<semantic-rule>' in the case's domain")

    truth = data.get("ground_truth") or {}
    basis = truth.get("basis")
    if basis not in BASES:
        problems.append(f"ground_truth.basis must be one of {BASES}, got {basis!r}")
    if basis == "runtime_proof" and not truth.get("runtime_script"):
        problems.append("ground_truth.basis is runtime_proof but no runtime_script is set")
    if basis in ("upstream_docs", "maintainer_statement") and not truth.get("citation"):
        problems.append(f"ground_truth.basis {basis!r} requires ground_truth.citation")
    if basis in ("php_semantics", "runtime_proof") and not truth.get("statement"):
        problems.append("ground_truth.statement is required to state what the code actually does")
    if basis == "runtime_proof":
        script = truth.get("runtime_script", "")
        if script and not os.path.exists(case.abs_path(script)):
            problems.append(f"runtime_script {script!r} does not exist")

    if not data.get("rule_class"):
        problems.append("rule_class must name the analyzer rule class under test")

    expect = data.get("expect") or {}
    for tool in (*TOOLS, *(['pzoom'] if 'pzoom' in expect else [])):
        exp = expect.get(tool)
        if exp is None:
            problems.append(f"expect.{tool} missing (use mode 'unsupported' with a reason)")
            continue
        mode = exp.get("mode")
        if mode not in MODES:
            problems.append(f"expect.{tool}.mode must be one of {MODES}, got {mode!r}")
            continue
        if mode == "unsupported":
            if not exp.get("reason"):
                problems.append(f"expect.{tool} is 'unsupported' without a reason")
            if not exp.get("citation"):
                problems.append(f"expect.{tool} is 'unsupported' without a citation")
        if mode == "diagnostics":
            if not exp.get("required"):
                problems.append(f"expect.{tool} mode 'diagnostics' needs a non-empty 'required' list")
            for item in exp.get("required", []):
                if not item.get("code") and not item.get("message_regex"):
                    problems.append(f"expect.{tool}.required entry needs 'code' or 'message_regex'")
            for item in exp.get("forbidden", []):
                if not item.get("code") and not item.get("message_regex"):
                    problems.append(f"expect.{tool}.forbidden entry needs 'code' or 'message_regex'")
        for item in exp.get("allowed", []):
            if not item.get("code") and not item.get("message_regex"):
                problems.append(f"expect.{tool}.allowed entry needs 'code' or 'message_regex'")
            if not item.get("reason"):
                problems.append(f"expect.{tool}.allowed entry needs a 'reason' - acknowledged output must be justified")
        # An expectation may name its own basis. That is how a fixture harvested
        # from one tool's test suite is judged for that tool (upstream_test) while
        # the other two are judged against the case's neutral ground truth.
        basis_override = exp.get("basis")
        if basis_override is not None:
            if basis_override not in BASES:
                problems.append(f"expect.{tool}.basis must be one of {BASES}, got {basis_override!r}")
            elif basis_override in ("upstream_docs", "maintainer_statement", "upstream_test") and not exp.get("citation"):
                problems.append(f"expect.{tool}.basis {basis_override!r} requires expect.{tool}.citation")

    if not os.path.exists(case.abs_path("composer.json")):
        problems.append("composer.json missing - the case must be runnable on its own")
    if not os.path.exists(case.abs_path("src")):
        problems.append("src/ missing - the fixture has no code")

    return problems


def to_json(case: Case) -> dict:
    return {"id": case.id, "path": case.path, "valid": not case.diagnostics,
            "problems": case.diagnostics}


def fingerprint(cases: list[Case]) -> str:
    """Identify the measured source bytes, independent of checkout location."""
    digest = hashlib.sha256()
    for case in sorted(cases, key=lambda item: item.id):
        root = Path(case.path)
        for path in sorted(root.rglob('*')):
            relative = path.relative_to(root)
            if (not path.is_file() or any(part in ('vendor', '.generated', '__pycache__')
                                          for part in relative.parts)):
                continue
            identity = f'{case.id}/{relative.as_posix()}'.encode()
            digest.update(identity + b'\0' + hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()
