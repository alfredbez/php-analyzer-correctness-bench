<?php
declare(strict_types=1);
/** @param list<int> $values */
function probe(int $value, array $values): int {
    if (!$value) {
        foreach ($values as $next) {
            if (!$value) { $value = $next; }
        }
    }
    return $value;
}
