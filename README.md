# PHP analyzer correctness benchmark

A low-cost, broad comparison of PHPStan, Psalm and Mago behavior.
**Not every benchmark expectation is desirable for every tool.** Warning policy,
legacy compatibility and annotation dialects are legitimate discussion points.

Each case is a small Composer project with an explicit baseline, sources and
runtime controls where applicable. FP and FN record disagreements with that
baseline, not necessarily implementation defects. This is not an overall ranking,
a real-project defect rate or a prescribed feature roadmap.

```
python3 harness/bench.py doctor            # which environment and tool versions
python3 harness/bench.py list              # the corpus
python3 harness/bench.py validate          # enforce the case contract
python3 harness/bench.py run --jobs 2      # run everything, write results/latest
python3 harness/bench.py run --case narrowing/is-int-on-string
```

Requirements: Docker (or a host PHP 8.2+), Python 3.10+, `tools/install.sh`
having pinned the analyzers into `tools/bin/`.
Dependency-backed cases also need PHP ZIP support or `unzip` in that runtime.
The installer prepares their locked Composer dependencies; lock files are part
of the corpus fingerprint.

Running a newer release without touching the pins:
`BENCH_TOOL_MAGO=/path/to/mago python3 harness/bench.py run --label drift`.
The same override exists for `BENCH_TOOL_PHPSTAN` and `BENCH_TOOL_PSALM`.
The report probes the selected binary, so its recorded version matches the run.
The nightly drift workflow uses `tools/install.sh --latest` in its fresh checkout.
Locally, use an out-of-tree `BENCH_TOOLS_DIR` to preserve the pinned binaries.

## Private review and version comparisons

This is a private working repository. Publication, maintainer contact and public
hosting require Alfred's explicit approval after he reviews the criteria and
report. No upstream issues or pull requests are created here.

The initial target is 120 semantic criteria, not 120 parameter variants.
`factory/catalog.json` lists 120 selected leads from Psalm, PHPStan and historical
Mago probes. `factory/assessment.json` accounts for every lead: a measured reduced
probe, coverage by an existing case, or an explicit deferral. Neither inventory
nor assessment implies exhaustive review of the upstream suites. Run
`python3 factory/catalog.py check` to verify the source-to-case mappings.

To compare an older release, current stable and an immutable main commit on
identical source bytes and PHP, without modifying the ordinary analyzer pins:

```
python3 tools/prepare-mago.py --config tools/mago-matrix.json
BENCH_PHP_IMAGE=php:8.4-cli python3 harness/compare.py --out results/comparisons/my-review
python3 harness/site.py --comparison results/comparisons/my-review/comparison.json --out results/comparisons/my-review/index.html
```

Preparing main needs Git, Cargo and the Rust toolchain required by its pinned
source. Release downloads currently target Linux x86_64. Main is built with the
recorded build profile; these measurements cannot support speed claims.
The output directory must be new, so measurements never overwrite one another.

Open `index.html` locally: it is a self-contained offline report with search,
domain and defect filters, version transitions, source fixtures, runtime checks,
expectations and measured diagnostics. It makes no external resource requests.
`comparison.json` is the machine-readable evidence bundle. Failed measurements,
changed corpora and policy exclusions cannot become fixes or regressions.

The [expanded review snapshot](results/comparisons/2026-10-18-expanded-review/index.html)
contains 142 runnable cases covering 127 declared semantic criteria. Of the 120
source candidates, 112 have new reduced probes and 7 map to existing cases.
One memory/performance candidate is deferred because its available fixture cannot
reproduce the resource defect. The snapshot measures Mago 1.54.0, 1.57.0 and pinned
main, plus PHPStan and Psalm, on PHP 8.4. Download the HTML to use it offline.
Earlier snapshots remain available for audit, including classifications corrected
after additional source or configuration evidence. Private GitHub Actions runs
also produce downloadable offline reports.

## What a result means

Four judgements enter the agreement denominator:

* **false negative** - the case requires a diagnostic and the analyzer is silent.
* **false positive** - the analyzer reports something the case forbids or that
  the case author did not acknowledge.
* **ok** - the analyzer did what the case requires.
* **mixed** - the analyzer both missed a required diagnostic and reported an
  unjustified diagnostic in the same case.

Two things are deliberately *not* counted:

* **by-design divergences.** Mago's maintainer has stated for several legacy
  patterns that he understands why PHPStan supports them and does not want them
  in Mago. Such an expectation is recorded as `unsupported` with a citation and
  appears in the matrix as `n/a`. PHPStan-specific `@phpstan-*` and Psalm-specific
  `@psalm-*` extensions are handled the same way.
* **tool errors, case errors, and skips.** Crashes and timeouts are failed
  measurements, invalid fixtures are case errors, and incompatible PHP versions
  are skipped. None enters the agreement denominator. Tool and case errors make
  the run command fail, so CI and the factory cannot treat them as a valid run.

The report always prints the denominator next to the rate, and lists every
divergence with its citation. A single aggregate number would hide exactly the
information the maintainer needs.

## Why a case is trustworthy

Each case declares where its ground truth comes from (`ground_truth.basis`):

| basis | meaning |
| --- | --- |
| `runtime_proof` | the case ships `runtime/check.php`; the fixture is executed and its real behaviour decides |
| `php_semantics` | the language reference decides, with a stated argument |
| `upstream_test` | taken from the analyzer's own test-suite expectation |
| `upstream_docs` | documented behaviour of the tool, with a citation |
| `maintainer_statement` | a maintainer said so, with a link |

`python3 harness/bench.py validate` rejects a case whose basis is a citation
without a citation, or a keyword without a statement. A case that cannot be
justified does not enter the corpus, because a benchmark is only as good as the
disagreements it refuses to make.

## For analyzer maintainers

The report is a starting point for discussion. Everything needed to check a
finding is in the repository:

```
python3 harness/bench.py gaps --tool mago      # everything mago got wrong, with evidence
python3 harness/bench.py run --case narrowing/is-int-on-string --tool mago
```

Every case directory is self-contained: `composer.json`, fixtures, and a
`case.json` that states the ground truth and where it comes from. The raw output
of every analyzer for every case is written to `results/runs/<run>/raw/<case>/`
during a run, so "the tool did not say that" can be checked instead of argued.

If a case's baseline is wrong or outside a tool's intended scope, contribute a
counterexample, citation or alternative configuration. A semantic fact and a
desirable diagnostic policy are separate questions. Nothing here is automatically
sent to an upstream maintainer.

## Layout

```
cases/<domain>/<slug>/     fixture + case.json + composer.json
harness/                   runner, adapters, classification, reporting
tools/versions.json        the pinned analyzer versions of the last run
results/runs/<run>/        SUMMARY.md, MATRIX.md, GAPS-<tool>.md, report.json
                           (the newest runs are committed; raw output is transient)
docs/                      methodology, case contract, classification rules
factory/                   the autonomous loop that grows the corpus
```

The newest committed run is the baseline the nightly drift job compares against;
nothing depends on a mutable "latest" pointer that two writers could fight over.

## Honest limitations

* Cases are deliberately small. A fixture proves that a rule fires or does not
  fire for one pattern; it does not prove how often the pattern occurs in a real
  codebase, and it does not measure precision over a corpus.
* The corpus is not balanced. It starts from real defects found in a ~10 year
  old, multi-million line legacy codebase, so "narrowing" and "legacy pattern"
  domains are over-represented relative to, say, generics.
* PHPStan is run at level 9 and Psalm at errorLevel 1 for every case. Analyzer
  levels are part of the expectation, not an accident: a case that is only
  expected to fire at a lower level says so in `config`.
* Runtime proofs are samples, not proofs. `runtime/check.php` demonstrates the
  behaviour for the values it tries; the exhaustive argument is the language
  reference quoted in the same case.

## Relation to the speed benchmark

`alfredbez/php-toolchain-benchmarks` (a fork of `carthage-software/php-toolchain-benchmarks`)
measures speed. This repository compares behavior against explicit baselines.
Neither substitutes for evaluating the tools on your own project.

## Contributing

External contributions are welcome: new reproducers, corrected expectations,
source citations, configuration comparisons and report improvements. Small,
independently runnable cases are easiest to discuss. Add cases under `cases/`,
explain the expected behavior, cite the evidence and run `validate` plus the case.
When proposing a different expectation, explain the semantic or policy reason;
a disagreement with this benchmark is not automatically a defect in the tool.

## License

MIT.
