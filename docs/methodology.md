# Methodology

## What is being measured

For every case and every analyzer, exactly one verdict:

| verdict | counted? | meaning |
| --- | --- | --- |
| `ok` | yes, positive | matched the case |
| `false_positive` | yes, negative | reported something the case forbids or did not claim |
| `false_negative` | yes, negative | stayed silent where the case requires a report |
| `mixed` | yes, negative | both of the above in one fixture |
| `divergence` | no | the rule class is not implemented by design; citation recorded |
| `tool_error` | no | crash, timeout, or unparseable output; the measurement failed |
| `skipped` | no | the case does not apply to the running PHP version |
| `case_error` | no | the case violates the contract; the corpus is broken, not the tool |

The published rate is `agreement = ok / (ok + false_positive + false_negative + mixed)`
with the denominator printed next to it. Cases that are divergences, errors or
skips are excluded from that denominator and shown separately, because folding
"not implemented on purpose" into "wrong" would be the same error as folding a
crash into a semantic correctness verdict. A crash can be an analyzer defect;
it remains visible as a tool error and makes the run command fail. It is not
relabelled as a case error merely because every selected analyzer failed.

## Rules that keep the number honest

1. **Ground truth before measurement.** A case states what the code does and why
   (`docs/case-contract.md`). The analyzers are then measured against it. If the
   expectation came from an analyzer's output instead, the benchmark would only
   measure agreement between tools, which is the thing this repository exists to
   avoid.
2. **Nothing is dropped silently.** A diagnostic that no predicate claims is
   either acknowledged under `allowed` with a reason, or counted. There is no
   "ignore unrelated output" switch.
3. **Strictness is declared, not accidental.** PHPStan runs at level 9 and Psalm
   at errorLevel 1 unless a case overrides it in `config`. The chosen setting is
   part of the case, and the report records the tool version next to every run.
4. **Divergences are quoted.** An `unsupported` expectation needs a citation to
   documentation or a maintainer statement. A tool is allowed to be different; it
   is not allowed to be different without saying so.
5. **Reproduce before believing.** `runtime/check.php` executes the fixture. A
   case whose runtime proof fails is a broken case, not a tool finding.

## What the numbers cannot tell you

* **Frequency.** A fixture proves that a rule fires or does not fire for one
  pattern. It says nothing about how often that pattern appears in real code, and
  nothing about precision over a large corpus.
* **Severity.** A false positive on a dead `is_int()` branch and a false positive
  on a public API call are counted the same. Severity is recorded per case in
  `rule_class`/`domain` and can be read per domain in the report.
* **Balance.** The corpus grows from whatever real defects were found, so
  domains are uneven by construction. The per-domain table exists for that
  reason; the headline number is a summary, not a ranking.

## Extended measures under discussion

Ideas that are not implemented yet, listed so nobody mistakes them for coverage:
precision over a labeled corpus, rule-level rather than case-level aggregation,
performance interaction (does raising the PHPStan level change findings), and
suppression handling (`@phpstan-ignore`, `@psalm-suppress`).
