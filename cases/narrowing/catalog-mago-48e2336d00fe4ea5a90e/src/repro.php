<?php
declare(strict_types=1);
function probe(int|string $left, float|string $right): string {
    if ($left === $right) {
        return strtoupper($left) . strtoupper($right);
    }
    return 'different';
}
