---
name: A case's ground truth is wrong
about: The benchmark judges an analyzer against a fixture whose stated behaviour is incorrect
title: "case <domain>/<slug>: <what is wrong>"
labels: benchmark-bug
---

## Case

`cases/<domain>/<slug>`

## What the case claims

(Quote `ground_truth.statement` and the expectation that is affected.)

## Why that is wrong

(The language reference, the runtime behaviour, or a link to documentation. If a
case's `runtime/check.php` passes but your argument still holds, say so - the
sample may be too narrow.)

## Suggested correction

(What should the ground truth and the expectations be?)
