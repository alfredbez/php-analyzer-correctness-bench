<?php
declare(strict_types=1);
function add(int $left, int $right): int { return $left + $right; }
/** @param array{int, int}|object $input */
function probe(array|object $input): int {
    return add(...$input);
}
