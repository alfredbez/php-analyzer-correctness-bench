# PHP analyzer correctness benchmark

Speed benchmarks for PHP analyzers are easy to produce and hard to interpret.
This repository measures the other axis: **is the analyzer right?**

Every case is a small, self-contained PHP fixture with a stated ground truth and
a stated expectation for PHPStan, Psalm and Mago. The harness runs all three
analyzers over the fixture and records what each one actually reported. The
result is a matrix of defects - false positives and false negatives - instead of
a stopwatch.

```
python3 harness/bench.py doctor            # which environment and tool versions
python3 harness/bench.py list              # the corpus
python3 harness/bench.py validate          # enforce the case contract
python3 harness/bench.py run --jobs 2      # run everything, write results/latest
python3 harness/bench.py run --case narrowing/is-int-on-string
```

Requirements: Docker (or a host PHP 8.2+), Python 3.10+, `tools/install.sh`
having pinned the analyzers into `tools/bin/`.

## What a result means

Only three judgements are counted:

* **false negative** - the case requires a diagnostic and the analyzer is silent.
* **false positive** - the analyzer reports something the case forbids or that
  the case author did not acknowledge.
* **ok** - the analyzer did what the case requires.

Two things are deliberately *not* counted:

* **by-design divergences.** Mago's maintainer has stated for several legacy
  patterns that he understands why PHPStan supports them and does not want them
  in Mago. Such an expectation is recorded as `unsupported` with a citation and
  appears in the matrix as `n/a`. PHPStan-specific `@phpstan-*` and Psalm-specific
  `@psalm-*` extensions are handled the same way.
* **tool errors and skips.** A crash, a timeout or a PHP version mismatch is an
  error in the harness, not a verdict about the analyzer.

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

## Layout

```
cases/<domain>/<slug>/     fixture + case.json + composer.json
harness/                   runner, adapters, classification, reporting
tools/versions.json        the pinned analyzer versions of the last run
results/runs/<run>/        SUMMARY.md, MATRIX.md, report.json (raw output is transient)
results/latest/            the newest published report
docs/                      methodology, case contract, classification rules
factory/                   the autonomous loop that grows the corpus
```

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
measures how fast the analyzers are. This repository measures how right they are.
Both are needed to decide what to adopt, and neither substitutes for the other.

## Contributing

Issues with a counter-example are the most valuable input: a fixture where the
recorded ground truth is wrong. Add the fixture under `cases/`, state the basis
and cite the evidence. Pull requests that only relax an expectation are not
accepted - change the ground truth or change nothing.

## License

MIT.
