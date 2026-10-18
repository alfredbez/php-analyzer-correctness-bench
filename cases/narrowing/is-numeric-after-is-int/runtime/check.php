<?php

declare(strict_types=1);

// Runtime side of the ground truth. The claim is about is_int() implying
// is_numeric(): for every int, is_numeric() is true. The int samples below are
// a sample, not an exhaustive proof - the exhaustive argument is that
// is_numeric() accepts any integer (language reference, is_numeric()) - but
// they do cover both signs, zero and the int boundaries, which is where a
// subtype relation would break if it were not a subtype relation.

require __DIR__ . '/../src/repro.php';

use function Bench\Narrowing\IsNumericAfterIsInt\classify;

$ints = [0, 1, -1, 5, 123, PHP_INT_MAX, PHP_INT_MIN];

foreach ($ints as $value) {
    if (!is_numeric($value)) {
        fwrite(STDERR, sprintf("is_numeric() is false for int %s\n", var_export($value, true)));
        exit(1);
    }
}

// The observable consequence: the `&& is_numeric($c)` operand never decides the
// branch, so classify() agrees with is_int() on every input.
$inputs = array_merge($ints, ['0', '123', '', 'abc', '1e3', ' 12 ', '-0', '12.5', '0x1A']);

foreach ($inputs as $value) {
    $expected = is_int($value) ? 'int' : 'other';
    if (classify($value) !== $expected) {
        fwrite(STDERR, sprintf("classify(%s) = %s, expected %s\n",
            var_export($value, true), classify($value), $expected));
        exit(1);
    }
}

printf("is_numeric() held for %d int sample(s); classify() followed is_int() for %d input(s)\n",
    count($ints), count($inputs));
exit(0);
