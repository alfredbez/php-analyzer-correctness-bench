<?php
declare(strict_types=1);
/** @param array{a: array<string, int>} $data
 * @return array{a: array{b: int, ...}} */
function probe(array $data): array {
    if (!isset($data['a']['b'])) { throw new LogicException(); }
    return $data;
}
