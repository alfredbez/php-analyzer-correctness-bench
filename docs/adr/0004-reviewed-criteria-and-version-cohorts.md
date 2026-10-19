# 0004 - Review criteria and compare immutable version cohorts

Date: 2026-10-18
Status: accepted; public repository and report approved on 2026-10-19

## Problem

Eighteen measured cases are a seed, not an adequate enterprise correctness
benchmark. The initial growth target of 57 is replaced by a release threshold of
at least 120 independently reviewed semantic criteria. Multiple values or
upstream examples of the same claim do not increase that count. Historical
reproducers, Psalm datasets and PHPStan fixtures are source candidates until
their meaning, configuration and independent oracle have been reviewed.

## Usage

```
python3 factory/catalog.py build
python3 tools/prepare-mago.py --config tools/mago-matrix.json
python3 harness/compare.py --config tools/mago-matrix.json --out results/comparisons/review
python3 harness/site.py --comparison results/comparisons/review/comparison.json --out results/comparisons/review/index.html
```

## Shape

The existing case manifests remain the source of benchmark expectations. A
source catalogue is a reproducible work queue, not scored coverage. Its entries
retain source identities and citations without copying upstream test suites.
Factory authors translate selected entries into small Composer projects with
runtime controls. Independent review checks semantic novelty as well as truth.

A comparison wraps ordinary harness runs. Each run records the exact corpus
fingerprint, PHP runtime, analyzer binary checksums and source references.
Historical, stable and main Mago binaries run against the same case bytes and
PHP runtime. Main means an immutable commit, never an unrecorded moving branch.
Changed corpora and failed measurements cannot count as fixes or regressions.

The static website reads those reports. It shows coverage, per-case
expectations, diagnostics, runtime evidence, reproduction commands, citations
and version transitions. It distinguishes source candidates, measured cases,
documented divergences and maintainer alignment. Internal review is not a
maintainer's acceptance of the benchmark's policy.

## Alternatives considered

Adding every Mago release as a new analyzer would duplicate expectations and
couple ordinary case authoring to version management. Instead, an outer cohort
comparison keeps the three analyzer families unchanged.

Importing entire upstream suites as benchmark fixtures would count harness
features, proprietary annotations and duplicate parameter variants as neutral
criteria. A source queue preserves that material for explicit translation and
curation instead.

## Tradeoffs

The initial comparison is deliberately smaller than the release threshold.
It demonstrates the measurement and review interface while the corpus grows.
An unsupported warning scope stays excluded unless evidence justifies changing
the expectation. A release build is not needed to compare correctness; the main
build profile is recorded and no speed conclusion is drawn.

Failed factory candidates are quarantined with their Git history and files.
Later rounds start from a fresh worktree rather than reusing failed output or
silently overwriting it. A quota failure still blocks that round's publication.

## Release gate

Alfred approved changing the repository to public and publishing the reviewed
report on GitHub Pages on 2026-10-19. Pages deploys only the checked-in reviewed
snapshot with the current template. Fresh CI and nightly measurements do not
automatically replace that snapshot.

Publication does not imply maintainer agreement with the expectations. No
automation may contact maintainers or create upstream PRs or issues. The factory
remains paused. A criterion count alone never authorizes a new release.
