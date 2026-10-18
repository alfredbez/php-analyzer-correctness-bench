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
same(probe(['arr'=>['ok'],'a'=>'','c'=>1]),'OK'); same(probe(['arr'=>[],'a'=>'','c'=>1]),'skip'); same(probe(['arr'=>['ok'],'a'=>'x','c'=>0]),'skip');
