<?php

declare(strict_types=1);

namespace Bench\Arrays\StrictInArrayNarrowing;

/** @param "a"|"b" $_ */
function accept_ab(string $_): void {}

/**
 * @param string|bool $x
 * @param list<"a"|"b"|int> $y
 */
function narrow(string|bool $x, array $y): void
{
    if (in_array($x, $y, true)) {
        accept_ab($x);
    }
}
