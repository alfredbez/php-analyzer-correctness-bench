# Agent protocol

Read this before touching the repository. It exists because most of the work here
is done by autonomous sessions, and an autonomous session that invents ground
truth poisons the corpus for everyone downstream.

## The four rules

1. **Ground truth first.** Every case states why it is right
   (`docs/case-contract.md`). "PHPStan reports X" is a measurement, not a ground
   truth. When you cannot justify an expectation from the language, the runtime,
   the tool's documented promise or a maintainer statement, do not write the case.
2. **Never relax an expectation to make a tool look better.** A false positive or
   a false negative in the matrix is the product. If a verdict surprises you, the
   answer is another `runtime/check.php` or a citation, never a wider predicate.
3. **Nothing lands without a run.** `python3 harness/bench.py validate` and
   `python3 harness/bench.py run --case <id>` must both have been executed, and
   the recorded verdicts must be what the tool actually produced. Raw tool output
   is in `results/runs/<run>/raw/<case>/<tool>.json` - read it, do not guess it.
4. **Small commits, one concern each.** A case addition, a harness fix and a
   documentation change are three commits with a one-line subject and, where the
   reason is not obvious, a body that says why.

## Scope discipline

* Code under `harness/` is shared. If you believe it must change, change it in
  the smallest possible way, add a unit test under `tests/`, and say in the commit
  body which verdict changed.
* Only touch `cases/**` when your task is authoring cases.
* Never edit `tools/versions.json` outside an explicit version-bump task.
* Never commit `tools/bin/*`, `results/runs/**/raw/`, `vendor/` or `.generated/`.

## Upstream relations

* Do not open automated upstream issues or pull requests against analyzer repositories. This benchmark measures and records behavior; it is not a tool for unsolicited upstream filings.
* The benchmark reports what it measures about a tool. It does not tell the
  maintainer what to do. A divergence is recorded with its citation; a defect is
  recorded as a defect; neither is a plan.

## Definition of done for a case

* `case.json`, `composer.json`, `src/` and, where possible, `runtime/check.php`
  exist.
* `python3 harness/bench.py validate` passes for the whole corpus.
* `python3 harness/bench.py run --case <id>` has been executed.
* Every verdict is either intended or explained in `notes`.
* The commit message names the rule class and the tool behaviour it records.
