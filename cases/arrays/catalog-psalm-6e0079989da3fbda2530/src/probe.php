<?php
declare(strict_types=1);
/** @param array<array-key> $values */
function consume(array $values): int {
    $sum = 0;
    foreach ($values as $value) { $sum += is_int($value) ? $value : strlen($value); }
    return $sum;
}
/** @return array<int, scalar> */
function produce(bool $bad): array { return $bad ? [false] : ['ok']; }
function probe(bool $bad): int { return consume(produce($bad)); }
