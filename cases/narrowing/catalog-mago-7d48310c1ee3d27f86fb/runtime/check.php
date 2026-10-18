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
same(seconds('min',true),'00.0'); same(seconds('max',false),'59'); fails(fn()=>seconds('other',false),ErrorException::class); ob_start(); finish(fn()=>'ok'); same(ob_get_clean(),'ok'); ob_start(); fails(function(){finish(function(): string { throw new Error('bad'); });},ErrorException::class); same(ob_get_clean(),'');
