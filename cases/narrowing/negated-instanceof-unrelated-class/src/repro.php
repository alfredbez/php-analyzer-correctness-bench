<?php

declare(strict_types=1);

namespace Bench\Narrowing\NegatedInstanceofUnrelatedClass;

class Alpha {}

class Beta {}

/**
 * Alpha and Beta are unrelated: neither extends the other, and PHP gives every
 * object exactly one inheritance chain. No instance of Alpha - nor of any
 * subclass of Alpha - is an instance of Beta, so the negation is always true.
 */
function is_not_beta(Alpha $value): bool
{
    return !($value instanceof Beta);
}
