<?php
declare(strict_types=1);
function probe(int|float $number): bool {
    if (empty($number)) { return false; }
    return true;
}
