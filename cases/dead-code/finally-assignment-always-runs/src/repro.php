<?php

declare(strict_types=1);

namespace Bench\DeadCode\FinallyAssignment;

/**
 * The inner `finally` block runs while the exception unwinds, before the outer
 * `catch` gets control, so $cleaned is true when the last statement reads it.
 * The ternary condition is therefore always true.
 */
function cleaned_flag(): int
{
    $cleaned = false;

    try {
        try {
            throw new \RuntimeException('a');
        } finally {
            $cleaned = true;
        }
    } catch (\Throwable) {
    }

    return $cleaned ? 1 : 0;
}
