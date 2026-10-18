<?php

declare(strict_types=1);

namespace Bench\LegacyPatterns\LooseComparisonWithZero;

/**
 * PHP 8 compares an int with a non-numeric string as two strings, so this
 * comparison is always false. Under PHP 7 the string was converted to a number
 * and the same comparison was always true - the classic legacy migration trap.
 * Under PHP 8 the branch below cannot be entered.
 */
function legacy_flag_is_set(): bool
{
    if ('abc' == 0) {
        return true;
    }

    return false;
}
