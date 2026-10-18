<?php

declare(strict_types=1);

namespace Bench\Assignability\CallableNotClosure;

function keep(\Closure $fn): \Closure
{
    return $fn;
}

function from_callable(callable $fn): \Closure
{
    return keep($fn);
}

function from_string_literal(): \Closure
{
    return keep('phpversion');
}

function from_closure(): \Closure
{
    return keep(static fn (): string => 'ok');
}
