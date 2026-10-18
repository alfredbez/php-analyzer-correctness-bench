<?php

declare(strict_types=1);

// Runtime side of the ground truth. The input domain is exactly {true} plus
// {string}: true is a bool, so is_bool() sends it into the early return, and a
// string is the only thing left for accept_string(). With strict_types on, a
// non-string reaching accept_string() would raise a TypeError, so the script
// fails if the narrowing assumption does not hold.

require __DIR__ . '/../src/repro.php';

use function Bench\Narrowing\IsBoolGuardExcludesTrue\quacks;

if (!is_bool(true)) {
    fwrite(STDERR, "is_bool() is false for true\n");
    exit(1);
}

$samples = [true, '', '0', 'false', 'true', 'abc'];

foreach ($samples as $sample) {
    quacks($sample);
}

printf("quacks() accepted %d sample(s) without a TypeError\n", count($samples));
exit(0);
