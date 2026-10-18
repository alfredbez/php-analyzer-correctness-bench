<?php

declare(strict_types=1);

namespace Bench\Narrowing\ObjectIsAlwaysTruthy;

final class Token
{
    public function value(): string
    {
        return 'secret';
    }
}

/**
 * Instances of the final user-defined Token class are truthy in a boolean
 * context. The negated condition is therefore always false and the branch is
 * dead. Internal classes with custom boolean casts are outside this domain.
 */
function is_falsy(Token $token): bool
{
    if (!$token) {
        return true;
    }

    return false;
}
