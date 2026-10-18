<?php

declare(strict_types=1);

// Runtime side of the ground truth: in the running PHP, comparing the literal
// 'abc' with the literal 0 is false, and the fixture's function therefore always
// leaves through its final return. PHP 7 converted the non-numeric string to 0
// and evaluated the same comparison as true; that rule is gone.

require __DIR__ . '/../src/repro.php';

use function Bench\LegacyPatterns\LooseComparisonWithZero\legacy_flag_is_set;

if ('abc' == 0) {
    fwrite(STDERR, "'abc' == 0 is true\n");
    exit(1);
}

if (legacy_flag_is_set()) {
    fwrite(STDERR, "legacy_flag_is_set() entered the unreachable branch\n");
    exit(1);
}

printf("'abc' == 0 evaluated to false and legacy_flag_is_set() returned false\n");
exit(0);
