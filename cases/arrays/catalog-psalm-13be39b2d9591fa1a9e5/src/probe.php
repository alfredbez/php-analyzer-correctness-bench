<?php
declare(strict_types=1);
/**
 * @param array<int, int> $first
 * @param array<int, int> $second
 * @param array<int, mixed> $input
 */
function probe(array $first, array $second, array $input): bool {
    if (!empty($input[0]) && !isset($second[$input[0]])) {
        return isset($first[$input[0]]);
    }
    return false;
}
