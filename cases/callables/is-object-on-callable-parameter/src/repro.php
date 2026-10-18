<?php

declare(strict_types=1);

namespace Bench\Callables\IsObjectOnCallableParameter;

function accept_object(object $_): void {}

final class Handler
{
    public function __invoke(): string
    {
        return 'handled';
    }
}

/**
 * A callable is a Closure, an object with __invoke, a function name or a
 * method array. The first two are objects, so is_object() has a reachable true
 * outcome for a declared callable parameter and the branch is not dead.
 */
function quacks(callable $fn): bool
{
    if (is_object($fn)) {
        accept_object($fn);

        return true;
    }

    return false;
}
