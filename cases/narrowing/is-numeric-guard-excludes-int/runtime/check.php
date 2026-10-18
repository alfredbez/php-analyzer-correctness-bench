<?php

declare(strict_types=1);

// Runtime side of the ground truth. The input domain is exactly {int} plus
// {string}, and the claim is that the int half never reaches accept_string():
//
// * for an int, is_numeric() is true, so the function returns early. The int
//   samples below cover both signs, zero and the boundaries.
// * for a string, the value that reaches accept_string() is a string by
//   definition, and accept_string() declares `string` with strict_types on, so
//   a non-string would raise a TypeError.
//
// The script therefore fails if any sample raises. PHP itself enforces the
// parameter type of accept_string(), which is what makes this observable.

require __DIR__ . '/../src/repro.php';

use function Bench\Narrowing\IsNumericGuardExcludesInt\quacks;

$samples = array_merge(
    [PHP_INT_MAX, PHP_INT_MIN, 0, 1, -1, 123],
    ['', '0', 'abc', '1e3', ' 12 ', '12a', '-0.0', '182312932139123123123']
);

foreach ($samples as $sample) {
    if (is_int($sample) && !is_numeric($sample)) {
        fwrite(STDERR, sprintf("is_numeric() is false for int %s\n", var_export($sample, true)));
        exit(1);
    }
}

foreach ($samples as $sample) {
    quacks($sample);
}

printf("quacks() accepted %d sample(s) without a TypeError\n", count($samples));
exit(0);
