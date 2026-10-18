<?php
declare(strict_types=1);

/** @param list<callable(string): int> $callbacks */
function invokeAll(array $callbacks): int {
    $total = 0;
    foreach ($callbacks as $callback) { $total += $callback('four'); }
    return $total;
}
function contextual(): int { return invokeAll([fn($value): int => strlen($value)]); }
