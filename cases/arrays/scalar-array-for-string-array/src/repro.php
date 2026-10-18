<?php

declare(strict_types=1);

namespace Bench\Arrays\ScalarArrayForStringArray;

/** @param array<string> $names */
function total_length(array $names): int
{
    $total = 0;
    foreach ($names as $name) {
        $total += strlen($name);
    }

    return $total;
}

/** @return array<int, scalar> */
function load(): array
{
    return [0 => 'ok', 1 => 1.5];
}

function main(): int
{
    return total_length(load());
}
