<?php
declare(strict_types=1);
final class Worker { public function run(): string { return 'ran'; } }
/** @param callable(): string $callback */
function invoke(callable $callback): string { return $callback(); }
function probe(): string {
    $callback = [new Worker(), 'run'];
    return invoke($callback);
}
