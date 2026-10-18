<?php
declare(strict_types=1);
/**
 * @param array<string, array{y?: int, width?: int}> $rows
 * @return array<array{y?: int, width?: int}>
 */
function probe(array $rows): array {
    array_multisort(array_column($rows, 'y'), SORT_ASC, $rows);
    return $rows;
}
