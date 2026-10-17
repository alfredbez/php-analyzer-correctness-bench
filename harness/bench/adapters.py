"""Adapters: tool output -> one diagnostic shape.

Every adapter returns:

    {"diagnostics": [ {code, message, file, line, severity} ], "tool_error": str|None}

Normalisations that are not obvious are documented here with the evidence that
forced them, because a silent normalisation is how a benchmark starts lying.

* mago JSON reports 0-based lines. ``mago analyze --reporting-format json`` on a
  fixture whose ``is_int()`` call sits on line 8 returns ``start.line: 7``,
  while ``mago analyze`` (rich) prints ``8`` in the same run and PHPStan and
  Psalm both report 8. The adapter therefore adds 1. See
  ``cases/narrowing/is-int-on-string``.
"""

from __future__ import annotations

import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTAINER_MOUNT = "/bench"


def _relative(path: str) -> str:
    """Reduce any absolute path to a repository-relative one."""
    for prefix in (CONTAINER_MOUNT + "/", ROOT + "/"):
        if path.startswith(prefix):
            return path[len(prefix):]
    return path.lstrip("/")


def _first_json_document(text: str):
    """Extract the first JSON document from a stream that may carry log noise."""
    decoder = json.JSONDecoder()
    for match in re.finditer(r"[\[{]", text):
        try:
            value, _ = decoder.raw_decode(text[match.start():])
            return value
        except ValueError:
            continue
    return None


def parse_phpstan(stdout: str, stderr: str) -> dict:
    payload = _first_json_document(stdout)
    if payload is None:
        return {"diagnostics": [], "tool_error": (stderr or stdout or "no output").strip()[:400]}
    diagnostics = []
    for path, entry in (payload.get("files") or {}).items():
        for message in entry.get("messages", []):
            diagnostics.append({
                "code": message.get("identifier") or "",
                "message": (message.get("message") or "").strip(),
                "file": _relative(path),
                "line": message.get("line"),
                "severity": "error" if not message.get("ignorable") else "warning",
            })
    errors = payload.get("errors") or []
    tool_error = None
    if errors:
        tool_error = "; ".join(str(item) for item in errors)[:400]
    return {"diagnostics": diagnostics, "tool_error": tool_error}


def parse_psalm(stdout: str, stderr: str) -> dict:
    payload = _first_json_document(stdout)
    if payload is None or isinstance(payload, dict):
        return {"diagnostics": [], "tool_error": (stderr or stdout or "no output").strip()[:400]}
    diagnostics = []
    for item in payload:
        diagnostics.append({
            "code": item.get("type") or "",
            "message": (item.get("message") or "").strip(),
            "file": _relative(item.get("file_path") or item.get("file_name") or ""),
            "line": item.get("line_from"),
            "severity": item.get("severity") or "error",
        })
    return {"diagnostics": diagnostics, "tool_error": None}


def parse_mago(stdout: str, stderr: str) -> dict:
    payload = _first_json_document(stdout)
    if payload is None or not isinstance(payload, dict) or "issues" not in payload:
        return {"diagnostics": [], "tool_error": (stderr or stdout or "no output").strip()[:400]}
    diagnostics = []
    for issue in payload.get("issues") or []:
        annotations = issue.get("annotations") or []
        span = (annotations[0].get("span") if annotations else None) or {}
        file_id = span.get("file_id") or {}
        line = (span.get("start") or {}).get("line")
        diagnostics.append({
            "code": issue.get("code") or "",
            "message": (issue.get("message") or "").strip(),
            "file": _relative(file_id.get("path") or file_id.get("name") or ""),
            "line": None if line is None else int(line) + 1,  # mago emits 0-based lines
            "severity": (issue.get("level") or "error").lower(),
        })
    return {"diagnostics": diagnostics, "tool_error": None}


ADAPTERS = {"phpstan": parse_phpstan, "psalm": parse_psalm, "mago": parse_mago}
