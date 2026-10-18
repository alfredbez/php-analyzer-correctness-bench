<?php

declare(strict_types=1);

namespace Bench\Narrowing\IsNumericAfterIsInt;

/**
 * The right operand of && can never change the result once the left operand
 * has been evaluated: is_int($c) narrows $c to int, and is_numeric() is true
 * for every int. The second call is therefore redundant, and the whole
 * condition is decided by is_int($c) alone.
 */
function classify(int|string $c): string
{
    if (is_int($c) && is_numeric($c)) {
        return 'int';
    }

    return 'other';
}
