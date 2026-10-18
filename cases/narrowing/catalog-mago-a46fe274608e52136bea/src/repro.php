<?php
declare(strict_types=1);
/** @param list<mixed> $values */
function probe(mixed $value, array $values): mixed {
    if (empty($value)) {
        foreach ($values as $next) {
            if (empty($value)) { $value = $next; }
        }
    }
    return $value;
}
