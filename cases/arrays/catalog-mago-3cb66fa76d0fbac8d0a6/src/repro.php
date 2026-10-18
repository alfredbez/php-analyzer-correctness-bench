<?php
declare(strict_types=1);
/** @param array<int, string> $left
 * @param array<int, string> $right */
function probe(array $left, array $right): string {
    if ($left === $right) {
        return implode(',', $left);
    }
    return 'different';
}
