<?php
declare(strict_types=1);
/** @param array<array-key, int> $values */
function sumInts(array $values): int {
    $sum=0; foreach ($values as $value) { $sum += $value; } return $sum;
}
/** @param array<array-key, mixed> $values */
function probe(array $values): int {
    if (is_array($values)) {
        return sumInts($values);
    }
    return 0;
}
