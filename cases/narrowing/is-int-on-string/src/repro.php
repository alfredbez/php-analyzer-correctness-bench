<?php

declare(strict_types=1);

namespace Bench\Narrowing\IsIntOnString;

/**
 * is_int() is only ever true for an int. A parameter that is declared as
 * string therefore makes the branch below unreachable, and the caller learns
 * nothing from the check. An analyzer that stays silent hides a real logic
 * error in the code under review.
 */
function classify(string $value): string
{
    if (is_int($value)) {
        return 'integer';
    }

    return 'string';
}
