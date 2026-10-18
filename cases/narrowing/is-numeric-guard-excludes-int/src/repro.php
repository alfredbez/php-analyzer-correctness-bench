<?php

declare(strict_types=1);

namespace Bench\Narrowing\IsNumericGuardExcludesInt;

function accept_string(string $_): void {}

/**
 * is_numeric() is true for every int, so an int can never reach the code after
 * the guard: the parameter is a string there and accept_string() is satisfied.
 */
function quacks(int|string $value): void
{
    if (is_numeric($value)) {
        return;
    }

    accept_string($value);
}
