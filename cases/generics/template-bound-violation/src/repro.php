<?php

declare(strict_types=1);

namespace Bench\Generics\TemplateBoundViolation;

use ArrayObject;

/**
 * @template T of \Countable
 *
 * @param T $value
 */
function count_all(mixed $value): int
{
    return count($value);
}

function count_three(): int
{
    return count_all([1, 2, 3]);
}

function count_object(): int
{
    return count_all(new ArrayObject([1, 2, 3]));
}
