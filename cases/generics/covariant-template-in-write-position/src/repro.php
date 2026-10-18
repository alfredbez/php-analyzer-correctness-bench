<?php

declare(strict_types=1);

namespace Bench\Generics\CovariantTemplateInWritePosition;

class Animal
{
}

final class Dog extends Animal
{
}

final class Cat extends Animal
{
}

/**
 * @template-covariant T
 */
final class Bag
{
    /** @param T $value */
    public function __construct(private mixed $value)
    {
    }

    /** @param T $value */
    public function push(mixed $value): void
    {
        $this->value = $value;
    }

    /** @return T */
    public function get(): mixed
    {
        return $this->value;
    }
}

/** @param Bag<Animal> $bag */
function put_cat(Bag $bag): void
{
    $bag->push(new Cat());
}

/** @param Bag<Dog> $dogs */
function adopt(Bag $dogs): Dog
{
    put_cat($dogs);

    return $dogs->get();
}

function run(): Dog
{
    return adopt(new Bag(new Dog()));
}
