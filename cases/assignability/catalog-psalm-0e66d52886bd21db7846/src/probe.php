<?php
declare(strict_types=1);
/**
 * @param numeric-string $number
 * @param non-empty-string $suffix
 * @return non-falsy-string
 */
function probe(string $number, string $suffix): string {
    return $number . $suffix;
}
/**
 * @param numeric-string $number
 * @param non-empty-string $prefix
 * @return non-falsy-string
 */
function reversed(string $number, string $prefix): string {
    return $prefix . $number;
}
