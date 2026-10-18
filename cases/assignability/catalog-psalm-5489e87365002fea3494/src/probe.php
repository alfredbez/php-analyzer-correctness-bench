<?php
declare(strict_types=1);
/**
 * @param non-empty-string $left
 * @param non-empty-string $right
 * @return non-falsy-string
 */
function probe(string $left, string $right): string {
    return $left . $right;
}
