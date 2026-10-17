# 0001 - Measure correctness, not speed

Date: 2026-10-17
Status: accepted

## Context

A fork of `carthage-software/php-toolchain-benchmarks` already measures how fast
PHP formatters, linters and analyzers are on three large projects. Speed is easy
to measure and easy to publish, and Mago's headline claim is being roughly an
order of magnitude faster than PHPStan and Psalm.

While adopting Mago on a ten-year-old, multi-million line legacy codebase, the
more consequential differences showed up elsewhere: diagnostics that were
missing on code that is genuinely wrong, and diagnostics reported on code that is
fine. For an enterprise migration the second kind is what stops the rollout -
every false positive costs a human decision, every false negative costs an
incident later.

## Decision

This repository measures correctness only: per case, per analyzer, false
positives and false negatives, with a stated ground truth. Speed
characteristics are explicitly out of scope and stay in the other repository.

## Consequences

* Every case must carry a ground truth and its basis, which makes case authoring
  slower than collecting tool output.
* The report is a defect list per tool (`GAPS-<tool>.md`), not a ranking, because
  a ranking would reward whichever analyzer reports the most.
* Cases are small and synthetic. Precision over a real codebase is not measured
  here and is not claimed.
