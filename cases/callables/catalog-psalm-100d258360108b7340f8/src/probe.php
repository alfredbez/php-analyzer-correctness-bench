<?php
declare(strict_types=1);
class Greeter {
    public static function greet(string $name = 'world'): string { return 'hello ' . $name; }
}
function probe(): mixed {
    $method = new ReflectionMethod(Greeter::class, 'greet');
    return $method->invoke(null, 'reader');
}
