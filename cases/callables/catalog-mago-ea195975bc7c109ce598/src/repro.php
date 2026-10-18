<?php
declare(strict_types=1);
/** @param array{test: string} $value */
function keyed(array $value): string { return $value['test']; }
function probe(callable $callback): string {
    if (is_array($callback)) { return keyed($callback); }
    return 'not-array';
}
final class Worker { public function run(): void {} }
