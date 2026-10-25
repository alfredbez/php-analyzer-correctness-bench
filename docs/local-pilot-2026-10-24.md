# Local benchmark and harvester pilot, October 24

This pilot extends the existing factory. It does not publish a replacement
website, start the timer, contact maintainers, or produce upstream contributions.
The personal Mago PR freeze and global factory policies remain unchanged.

## Corpus and source inventory

The corpus grows from 142 cases and 127 declared criteria to 144 cases and 129
criteria. The two additions are independent reductions from unused public test
leads. Their expectations follow native PHP semantics, not another analyzer's
output:

| Criterion | Controls | New batch observation |
| --- | --- | --- |
| `assignability/bitwise-not-boolean-operand` | Both booleans throw; integer and byte-string complements succeed | PHPStan and Psalm report the invalid operand; Mago 1.58.2 is silent |
| `assignability/native-readonly-property-reassignment` | Two objects initialize independently; same-value and changed-value writes throw and preserve state | All three established analyzers report the forbidden write |

The nearest existing boolean-narrowing criteria do not test an operator's input
domain. The existing asymmetric-property-override criterion concerns declaration
compatibility, not an initialized property's write-once state. These distinctions
are recorded in `factory/assessment.json` rather than inferred from new filenames.

The main catalog now accounts for 122 leads: 114 measured reductions, seven
covered by existing cases, and one deferred resource experiment. All original
candidate and assessment records are retained. The factory's domain targets
remain unchanged.

`results/harvest/2026-10-24/` contains a separate expansion snapshot of the same
inventory, with 80 fresh public leads appended. It records 40 Psalm and 40 PHPStan
leads as `pending`. These leads have ID and probe-hash deduplication, not semantic
acceptance. Its assessment gate deliberately fails until each has a justified
outcome. Do not count these 80 leads as criteria, findings, or reviewed tests.

The extraction inventories 8,410 named Psalm datasets and 4,938 PHPStan fixture
files at the existing pinned source revisions. This is not exhaustive semantic
review of either suite. See `factory/SOURCES.md` for revisions and licenses.

## Refreshed measurement

The local stable run uses PHP 8.4.27 in Docker and these release pins:

| Tool | Version |
| --- | --- |
| PHPStan | 2.3.1 |
| Psalm | 6.20.1, commit `376425b8e67b79773add388e16b4f6be5693dc87` |
| Mago | 1.58.2 |

The final full-corpus snapshot is `results/runs/2026-10-24-stable-final/`.
It records binary hashes, runtime proofs, selected cases, and the exact corpus
fingerprint. Findings remain disagreements with this corpus's baseline, not an
overall tool ranking or an estimate of real-project defect rates.

The final run and report audit pass. It contains 432 analyzer results, including
three expected skips for the one PHP-8.2-only case. All 429 executed analyzer
processes have accepted exit codes and no raw tool errors, including excluded
by-design rows. Runtime checks pass for 143 applicable cases, with no failed
proof. The final fingerprint matches the current 144-case corpus.

All 54 unit tests pass, as do corpus validation and the 122-lead assessment
check. The new cases' runtime controls also pass independently on PHP 8.2.35,
8.3.36, 8.4.27 and 8.5.12. The pending-lead assessment and Pzoom report audit
both fail deliberately, confirming that incomplete work cannot pass those checks.

The public October 18 comparison and `tools/mago-matrix.json` remain historical.
No claim is made that their fixed-main binary is current. This pilot refreshes
the stable release measurement, not that historical main profile. The changed PHP
patch release and expanded corpus also prevent treating aggregate differences
from that snapshot as measured fixes or regressions.

## Pzoom is integrated but not ready to score

The opt-in adapter and installer use unmodified
`muglug/pzoom@c8162978033745e585f8e60d15a66a48862333cc`, also the remote HEAD
observed on October 24. Its README explicitly promises no support. The installer
pins dependency resolution with `tools/pzoom-Cargo.lock` and retains the MIT
license beside the binary. The experiment's build receipt is
`results/runs/2026-10-24-new-batch-final/pzoom-provenance.json`.

The local build succeeds. Three integration facts matter:

1. Pzoom accepts `--format json`, but this revision never uses that field when
   rendering output. It also has no working `--version` probe. The harness checks
   console error and info counts, the completion footer, exit status, and binary
   provenance instead of accepting an empty parse as success.
2. Passing the project root can analyze runtime control files when relative XML
   directories do not resolve as expected. The adapter now passes explicit
   `analyze` targets, keeping runtime diagnostics out of the measurement.
3. Every pilot invocation reports scan errors from its embedded
   `stubs/extensions/sockets.phpstub`. The byte offset in the actual error points
   to `const SKF_AD_OFF = -096;`, an invalid octal literal. Bundled extension
   stubs are mandatory in `Scanner::scan_stubs_for_php_version`; only the
   `extensions/optional/` subtree is configurable. Trying a socket-disable XML
   entry neither prevents Pzoom's scan nor passes Psalm's config schema. That
   experiment was removed from the fixtures.

The final two-case run therefore records **two Pzoom tool errors and no judged
Pzoom cases**, even though its partial output contains plausible diagnostics.
The report audit fails with those errors and an empty denominator. This failure
is intentional evidence that publication gates reject partial measurements.
The captured regression fixture is `tests/fixtures/pzoom-stub-scan-error.json`.
No patched binary, suppressed scan error, or inherited Psalm expectation makes
the experiment green.

Pzoom's documented case-sensitive resolution and statement-level return
diagnostics differ from Psalm. Future cases need explicit Pzoom expectations and
citations for deliberate divergences. No expectation on an older case means an
unscored observation, not evidence that Pzoom deliberately does not support it.

## Reproduction and gates

```
./tools/install.sh
python3 -m unittest discover -s tests -t . -q
python3 harness/bench.py validate
python3 factory/catalog.py check
python3 harness/bench.py run --php 8.4 --jobs 2 --output results/runs/my-stable-check
python3 harness/bench.py audit --report results/runs/my-stable-check/report.json
python3 factory/catalog.py expand --limit-per-family 40 \
  --out results/harvest/my-check/catalog.json \
  --assessment-out results/harvest/my-check/assessment.json
```

The independent review receipt lives with the final stable snapshot. It records
the reviewer model, scope, rerun evidence, and reviewed file hashes. The review
does not turn pending leads into accepted criteria or Pzoom errors into findings.

The read-only Kimi review accepts the two-case core batch and the fail-closed
experimental adapter. It independently reruns the runtime proofs, both default
and four-tool batches, unit tests, source hashes and the report gates. Its
zero-denominator wording finding is fixed in the shared gap renderer and covered
by a regression test. A separate follow-up reviews that small correction.

Two review observations need context, not data changes. Refreshing release pins
implements this task's explicit request to update the old measurement basis.
The catalog's retained `history_ledger_sha256` identifies the original historical
ledger snapshot; the live ledger has since changed. Public-source expansion does
not use that historical ledger as a current source of truth.

Alfred subsequently approved integrating and pushing this reviewed pilot to the
benchmark repository's `main`. The local review receipt predates that approval
and describes the then-uncommitted source snapshot. Publication of these files
does not replace the public website's historical comparison.

## Decisions before unattended operation

Pzoom remains an experiment until its unchanged source completes without scan
errors. Updating its pin or maintaining a separately labeled patched build needs
a separate choice. No upstream issue or support request is implied.

The remaining 80 leads need semantic triage and small independently reviewed
batches. Raw extraction is not permission to increase factory targets. Expanding
the targets, enabling the timer, or replacing the public snapshot each remains a
separate decision. Publishing this benchmark does not authorize upstream contact
or contributions.
