# Seed material for new cases

Four sources, in descending order of usefulness. All of them are local; do not
download the internet when a checkout is already there.

## 1. Field findings from a real legacy codebase

`/home/abez/projects/mago-upstream-prep/repro/` - about 200 single-file fixtures
found while analyzing a ten-year-old, multi-million line codebase, plus
`repro/README.md`. `psalm-harvest-*` directories in the same folder are patterns
taken from Psalm's own expectations.

Caveat: the comments in those files were written by an earlier agent and are
**not** ground truth. Re-derive the behaviour, run it, and cite the language or
the runtime. Several of the bugs they describe have been fixed upstream since.

## 2. Mago's analyzer test suite

`/home/abez/projects/mago-upstream-prep/mago/crates/analyzer/tests/cases/*.php`
with the harness in `crates/analyzer/tests/`. Mago's own expectations for these
fixtures are evidence **for Mago** (`expect.mago.basis: "upstream_test"` with the
file as citation). Whether PHPStan or Psalm should also report is a separate
question that needs the language, not Mago's suite.

## 3. PHPStan's type-inference fixtures

`/home/abez/projects/phpstan-src/tests/PHPStan/Analyser/nsrt/*.php` (about 1800
files) encode PHPStan's intended inference with `assertType()`. Evidence **for
PHPStan**, same reasoning as above. These are the best source for narrow,
well-documented inference behaviour - and the best source for finding cases where
a *different* analyzer's inference contradicts a documented expectation.

## 4. Psalm's issue documentation and test suite

`/home/abez/projects/psalm-src` is available locally. The catalog pins the test
revision, independently of the Psalm binary version used for measurement.

`docs/running_psalm/issues/<Code>.md` documents each issue code with a small
example and a link; `tests/` holds the expectations. Evidence **for Psalm**.

## Balance rules

The corpus must not become a list of Mago's gaps. Aim for roughly equal numbers
of findings per tool:

* A case where the reference tools (PHPStan, Psalm) miss something that Mago
  catches is worth as much as the reverse.
* A case where PHPStan is wrong on its own documented promise is a legitimate
  finding.
* A case where all three are right is still useful as a regression guard - mark
  it clearly in `notes` and keep it, because it proves the corpus can produce a
  green row.

## What not to use as ground truth

* A comment in an existing repro directory.
* "Tool X reports ..." - a measurement, not a truth.
* A blog post, a benchmark table, or another analyzer's documentation about a
  different analyzer.
* Your own reasoning about what a good analyzer should do, unattached to PHP
  semantics and without a runtime check.

## Source revisions and licenses

The October 24 batch retains the existing clean source checkouts. It does not
claim that these tests represent the latest upstream suites:

| Source | Test revision | License |
| --- | --- | --- |
| Psalm | `62e52cd9fe3ab4429debc0eb0306057419b0a9d6` | MIT, Copyright 2016 Vimeo |
| PHPStan | `2c12dac5e4f8626c8a7cfc0b4bb9c5ce48d37c96` | MIT, Copyright 2016 Ondřej Mirtes and 2025 PHPStan s.r.o. |
| Pzoom experiment | `c8162978033745e585f8e60d15a66a48862333cc` | MIT, Copyright 2025–2026 Matt Brown |

New fixtures are independent minimal reductions, not copies of upstream test
bodies. Their manifests cite the original test, license, and PHP semantics.
If copying substantial source in future, retain the upstream copyright and full
MIT permission notice. The Pzoom installer retains its license beside the local
binary. Pzoom is a measured tool here, not an independent ground-truth source.

`catalog.py expand` uses the same extraction as the original catalog. Its ID and
probe-hash exclusions remove previously selected leads, not semantic duplicates.
Every new criterion still needs comparison against the existing corpus and an
independent review. Neither 8,410 Psalm datasets nor 4,938 PHPStan files means
that the entire corresponding suite has been semantically reviewed.
