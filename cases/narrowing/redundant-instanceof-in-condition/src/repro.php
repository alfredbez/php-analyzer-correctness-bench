<?php

declare(strict_types=1);

namespace Bench\Narrowing\RedundantInstanceofInCondition;

function is_exception(\RuntimeException $e): bool
{
    if ($e instanceof \Exception) {
        return true;
    }

    return false;
}
