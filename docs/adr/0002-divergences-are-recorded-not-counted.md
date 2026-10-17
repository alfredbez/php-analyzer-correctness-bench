# 0002 - Record by-design divergences instead of counting them as defects

Date: 2026-10-17
Status: accepted

## Context

The three analyzers do not have the same feature set, and two of the differences
are deliberate:

* PHPStan and Psalm support their own annotations (`@phpstan-*`, `@psalm-*`) and
  a set of legacy-friendly patterns that do not follow from strict type logic.
  Mago's maintainer has stated for several of these that he understands why they
  are supported but does not want them in Mago.
* Both reference tools accept patterns whose only justification is that a large
  body of existing code uses them.

A benchmark that counts these as defects produces a large, permanent, meaningless
number, and a maintainer who reads it learns nothing. A benchmark that silently
drops them hides a real gap.

## Decision

An expectation may be `mode: "unsupported"` with a `reason` and a `citation`.
Such a verdict is reported as a divergence, appears in the matrix as `n/a`, is
excluded from the agreement denominator, and is listed separately with its
citation. The validator rejects an `unsupported` expectation without a citation.

## Consequences

* The headline agreement number is computed over cases where the rule class is
  arguably in scope for the tool, and the denominator is always printed.
* A maintainer can overturn a divergence by pointing at the citation; the case
  then moves into the counted set. That conversation is the point of the
  repository.
* There is a judgement call per case. It is made visible in `case.json` instead
  of being buried in a script.
