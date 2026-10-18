<?php
declare(strict_types=1);
function probe(object $value): bool {
    $name = get_class($value);
    if ($name) { return true; }
    return false;
}
