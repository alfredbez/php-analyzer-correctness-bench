<?php

declare(strict_types=1);

namespace Bench\Narrowing\RedundantInstanceofOnDeclaredClass;

/**
 * RuntimeException extends Exception, so every value the parameter can hold is
 * already an Exception. The check cannot be false and cannot distinguish any
 * two inputs.
 */
function is_exception(\RuntimeException $e): bool
{
    return $e instanceof \Exception;
}
