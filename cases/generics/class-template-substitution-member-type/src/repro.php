<?php

declare(strict_types=1);

namespace Bench\Generics\ClassTemplateSubstitutionMemberType;

/** @template T */
final class Box
{
    /** @param T $value */
    public function __construct(private mixed $value)
    {
    }

    /** @return T */
    public function get(): mixed
    {
        return $this->value;
    }
}

final class Dog
{
    public function bark(): string
    {
        return 'woof';
    }
}

final class Cat
{
    public function meow(): string
    {
        return 'meow';
    }
}

/** @param Box<Dog> $box */
function bark_of_dog(Box $box): string
{
    return $box->get()->bark();
}

/** @param Box<Cat> $box */
function bark_of_cat(Box $box): void
{
    $box->get()->bark();
}

/** @param Box<Cat> $box */
function meow_of_cat(Box $box): string
{
    return $box->get()->meow();
}
