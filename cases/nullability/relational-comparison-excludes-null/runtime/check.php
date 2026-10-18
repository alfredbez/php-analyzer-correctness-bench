<?php

declare(strict_types=1);

// Runtime side of the ground truth. The input domain is {null} plus {int}, and
// the null case is a single value, so it can be checked directly: if null > 0
// is false, no null can reach the branch. For an int the comparison is an
// ordinary numeric comparison, and the script checks that the branch is
// actually entered (a vacuous proof would not show anything) and that
// accept_int() receives an int, which PHP enforces.

require __DIR__ . '/../src/repro.php';

use function Bench\Nullability\RelationalComparisonExcludesNull\quacks;

if (null > 0) {
    fwrite(STDERR, "null > 0 is true; null would enter the branch\n");
    exit(1);
}

if (null > -1) {
    fwrite(STDERR, "null/int comparison was numeric instead of boolean\n");
    exit(1);
}

foreach ([null, 0, -1, PHP_INT_MIN] as $sample) {
    if (quacks($sample) !== false) {
        fwrite(STDERR, sprintf("quacks(%s) entered the branch\n", var_export($sample, true)));
        exit(1);
    }
}

foreach ([1, 2, PHP_INT_MAX] as $sample) {
    if (quacks($sample) !== true) {
        fwrite(STDERR, sprintf("quacks(%s) did not enter the branch\n", var_export($sample, true)));
        exit(1);
    }
}

echo "null > 0 is false; quacks() entered the branch for positive ints only\n";
exit(0);
