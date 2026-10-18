<?php

declare(strict_types=1);

// Runtime side of the ground truth. The input domain is {null} plus {string}:
// null takes the early return, and everything that reaches accept_string() is a
// string, which PHP enforces through the declared parameter type.

require __DIR__ . '/../src/repro.php';

use function Bench\Nullability\IsNullGuardNarrowsAwayNull\quacks;

if (!is_null(null)) {
    fwrite(STDERR, "is_null() is false for null\n");
    exit(1);
}

$samples = [null, '', '0', 'abc'];

foreach ($samples as $sample) {
    quacks($sample);
}

printf("quacks() accepted %d sample(s) without a TypeError\n", count($samples));
exit(0);
