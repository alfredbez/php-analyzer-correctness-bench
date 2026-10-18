<?php

declare(strict_types=1);

namespace Bench\Nullability\IsNullGuardNarrowsAwayNull;

function accept_string(string $_): void {}

/**
 * is_null() is true only for the null half of ?string, so after the guard the
 * parameter is a string and accept_string() is satisfied.
 */
function quacks(?string $value): void
{
    if (is_null($value)) {
        return;
    }

    accept_string($value);
}
