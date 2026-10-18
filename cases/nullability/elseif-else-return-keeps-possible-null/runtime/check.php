<?php

declare(strict_types=1);

// Runtime side of the ground truth. The first sample is the decisive one: it
// reaches the final check with $b === null, so the check is neither redundant
// nor unreachable. The others show that the other reachable states still
// behave, which keeps the fixture from passing for the wrong reason.

require __DIR__ . '/../src/repro.php';

use function Bench\Nullability\ElseifElseReturnKeepsPossibleNull\is_null_after;

$cases = [
    ['value', null, true],   // first branch taken, $b never tested, still null
    [null, 'value', false],  // second branch taken, $b is non-null
    [null, null, false],     // else branch returns before the check
    ['a', 'b', false],       // first branch taken, $b is non-null
];

foreach ($cases as [$a, $b, $expected]) {
    $actual = is_null_after($a, $b);
    if ($actual !== $expected) {
        fwrite(STDERR, sprintf("is_null_after(%s, %s) = %s, expected %s\n",
            var_export($a, true), var_export($b, true), var_export($actual, true),
            var_export($expected, true)));
        exit(1);
    }
}

printf("is_null_after() reached the final check with null in %d case(s)\n", count($cases));
exit(0);
