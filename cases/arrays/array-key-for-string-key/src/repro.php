<?php

declare(strict_types=1);

namespace Bench\Arrays\ArrayKeyForStringKey;

/** @param array<string, int> $counts */
function render(array $counts): string
{
    $out = '';
    foreach ($counts as $name => $count) {
        $out .= strtoupper($name) . ':' . $count . ';';
    }

    return $out;
}

/** @return array<array-key, int> */
function load(): array
{
    return [0 => 1, 'users' => 2];
}

function main(): string
{
    return render(load());
}
