<?php
declare(strict_types=1);

use PHPStan\BetterReflection\Reflection\Adapter\ReflectionEnum;
use PHPStan\BetterReflection\Reflection\Adapter\ReflectionNamedType;

function backingType(ReflectionEnum $enum): ?ReflectionNamedType {
    return $enum->getBackingType();
}
