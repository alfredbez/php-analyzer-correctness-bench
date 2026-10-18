<?php
declare(strict_types=1);
require __DIR__ . '/../vendor/autoload.php';
require __DIR__ . '/../src/repro.php';

enum Number: int { case One = 1; }
enum Unit { case One; }
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
$reflector = (new PHPStan\BetterReflection\BetterReflection())->reflector();
$backed = new PHPStan\BetterReflection\Reflection\Adapter\ReflectionEnum($reflector->reflectClass(Number::class));
$unit = new PHPStan\BetterReflection\Reflection\Adapter\ReflectionEnum($reflector->reflectClass(Unit::class));
check(backingType($backed)?->getName() === 'int');
check(backingType($unit) === null);
