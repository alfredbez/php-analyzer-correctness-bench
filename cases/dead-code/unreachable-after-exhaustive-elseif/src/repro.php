<?php

declare(strict_types=1);

namespace Bench\DeadCode\UnreachableAfterExhaustiveElseif;

function classifyFlag(bool $flag): int
{
    if ($flag) {
        return 1;
    } elseif (!$flag) {
        return 2;
    }

    return 3;
}
