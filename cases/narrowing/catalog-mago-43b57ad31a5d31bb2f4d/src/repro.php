<?php
declare(strict_types=1);
function probe(int $value): bool {
    if ($value !== null && $value !== true && $value !== false) {
        return $value !== 5;
    }
    return false;
}
