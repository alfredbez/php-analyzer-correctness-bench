<?php

declare(strict_types=1);

namespace Bench\Generics\TemplateInferenceFromArgument;

/**
 * @template T
 *
 * @param T $value
 *
 * @return T
 */
function identity(mixed $value): mixed
{
    return $value;
}

function length_of_int(): int
{
    return strlen(identity(5));
}

function length_of_string(): int
{
    return strlen(identity('abc'));
}
