<?php
declare(strict_types=1);
/** @param array<array-key, mixed> $value */
function needsArray(array $value): int { return count($value); }
function probe(mixed $value): int {
    if (!is_array($value) && !empty($value)) {
        return needsArray($value);
    }
    return 0;
}
