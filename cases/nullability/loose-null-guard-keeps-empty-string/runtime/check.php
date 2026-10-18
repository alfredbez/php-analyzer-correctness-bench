<?php

declare(strict_types=1);

// Runtime side of the ground truth. The claim is a reachability claim about the
// inner check, and the samples below decide it: '' is loosely equal to null but
// not strictly equal, so classify('') must leave the inner if on its false
// path. '0' is the interesting control - in PHP 8 it is NOT loosely equal to
// null, so it must not enter the outer branch at all.

require __DIR__ . '/../src/repro.php';

use function Bench\Nullability\LooseNullGuardKeepsEmptyString\classify;

$cases = [
    [null, 'null'],
    ['', 'loose-null'],
    ['0', 'string'],
    ['abc', 'string'],
];

foreach ($cases as [$value, $expected]) {
    $actual = classify($value);
    if ($actual !== $expected) {
        fwrite(STDERR, sprintf("classify(%s) = %s, expected %s\n",
            var_export($value, true), $actual, $expected));
        exit(1);
    }
}

$loose = '' == null;
$strict = '' === null;

if ($loose !== true || $strict !== false) {
    fwrite(STDERR, "the loose/strict difference for '' does not hold\n");
    exit(1);
}

printf("classify() distinguished null from '' on %d sample(s)\n", count($cases));
exit(0);
