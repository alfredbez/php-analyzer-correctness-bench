<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
set_error_handler(static function(int $level, string $message): never { throw new ErrorException($message, 0, $level); });
function same(mixed $actual, mixed $expected): void {
    if ($actual !== $expected) { throw new RuntimeException('Mismatch: '.var_export([$actual,$expected],true)); }
}
function fails(callable $action, string $class): void {
    try { $action(); } catch (Throwable $error) {
        if ($error instanceof $class) { return; }
        throw $error;
    }
    throw new RuntimeException('Expected '.$class);
}
same(strings(['foo'=>'x']),true); same(strings(['foo'=>'x','bar'=>'y']),false); same(integers([0=>'x']),true); same(integers([0=>'x',1=>'y']),false);
