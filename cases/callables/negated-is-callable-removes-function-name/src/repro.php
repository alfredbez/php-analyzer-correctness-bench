<?php

declare(strict_types=1);

namespace Bench\Callables\NegatedIsCallableRemovesFunctionName;

/** @param list<int> $_ */
function accept_array(array $_): void {}

/**
 * The value is either the function name 'strlen' or the array [1]. is_callable()
 * is true for the function name and false for [1], which is not a valid
 * callback array, so the code after the guard only ever sees [1] and
 * accept_array() is satisfied.
 */
function quacks(bool $useFunctionName): void
{
    $value = $useFunctionName ? 'strlen' : [1];

    if (is_callable($value)) {
        return;
    }

    accept_array($value);
}
