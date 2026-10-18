<?php

declare(strict_types=1);

namespace Bench\Nullability\ElseifElseReturnKeepsPossibleNull;

/**
 * Execution continues past the structure when at least one of the two
 * conditions held - not when both did. With $a !== null and $b === null the
 * first branch runs, $b was never tested, and the final check still has a true
 * outcome.
 */
function is_null_after(?string $a, ?string $b): bool
{
    if ($a !== null) {
        $a = trim($a);
    } elseif ($b !== null) {
        $b = trim($b);
    } else {
        return false;
    }

    return $b === null;
}
