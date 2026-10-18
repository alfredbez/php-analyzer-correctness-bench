<?php
declare(strict_types=1);
function probe(mixed $value, bool $right): bool {
    if (!$value) { return false; }
    return $value && $right;
}
