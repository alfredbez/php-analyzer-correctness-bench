<?php

declare(strict_types=1);

namespace Bench\Assignability\DocblockReturnCovariance;

class Animal {}

class Dog extends Animal
{
    public function bark(): string
    {
        return 'woof';
    }
}

class Cat extends Animal {}

class Shelter
{
    /** @return Dog */
    public function adopt(): Animal
    {
        return new Dog();
    }
}

class BadShelter extends Shelter
{
    /** @return Animal */
    #[\Override]
    public function adopt(): Animal
    {
        return new Cat();
    }
}

function wake(Shelter $shelter): string
{
    $animal = $shelter->adopt();

    return $animal->bark();
}
