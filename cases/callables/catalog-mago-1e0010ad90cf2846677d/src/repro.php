<?php
declare(strict_types=1);
function probe(callable $callback): string {
    if (is_string($callback)) { return strtoupper($callback); }
    if (is_object($callback)) { return get_class($callback); }
    return 'array';
}
final class Worker { public static function run(): void {} }
