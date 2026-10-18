<?php

declare(strict_types=1);

namespace Bench\Narrowing\IsBoolGuardExcludesTrue;

function accept_string(string $_): void {}

/**
 * true is a bool, and is_bool() is true for it, so the literal true can never
 * reach the code after the guard: the parameter is a string there and
 * accept_string() is satisfied.
 */
function quacks(string|true $value): void
{
    if (is_bool($value)) {
        return;
    }

    accept_string($value);
}
