<?php

declare(strict_types=1);

namespace Bench\Nullability\LooseNullGuardKeepsEmptyString;

/**
 * The loose comparison is true for null and for the empty string, so inside the
 * branch the strict `=== null` check still has a reachable false outcome: it is
 * not redundant, and the code after it runs for ''.
 */
function classify(?string $value): string
{
    if ($value == null) {
        if ($value === null) {
            return 'null';
        }

        return 'loose-null';
    }

    return 'string';
}
