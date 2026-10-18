<?php
declare(strict_types=1);
class Known {}
/** @param class-string $class */
function instantiate(string $class): object { return new $class(); }
function guarded(string $name): ?object {
    if ($name === Known::class) { return instantiate($name); }
    return null;
}
