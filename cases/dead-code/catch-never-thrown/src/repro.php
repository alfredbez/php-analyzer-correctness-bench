<?php

declare(strict_types=1);

namespace Bench\DeadCode\CatchNeverThrown;

final class UnusedDomainException extends \Exception
{
}

function doubleValue(int $count): int
{
    try {
        return $count * 2;
    } catch (UnusedDomainException) {
        return 0;
    }
}
