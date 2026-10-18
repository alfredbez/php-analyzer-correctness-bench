<?php

declare(strict_types=1);

namespace Bench\Nullability\RelationalComparisonExcludesNull;

function accept_int(int $_): void {}

/**
 * When null is compared with an integer, both operands convert to bool.
 * false > false is false, so null never enters the branch: inside it the
 * parameter is an int and accept_int() is satisfied.
 */
function quacks(?int $value): bool
{
    if ($value > 0) {
        accept_int($value);

        return true;
    }

    return false;
}
