<?php
declare(strict_types=1);
/** @param array{a: mixed, b: mixed} $row */
function probe(array $row): bool {
    if (!empty($row['a']) && !empty($row['b']['c'])) {
        return true;
    }
    return false;
}
