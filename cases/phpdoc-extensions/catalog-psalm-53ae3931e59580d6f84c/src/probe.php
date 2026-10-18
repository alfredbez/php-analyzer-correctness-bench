<?php
declare(strict_types=1);
class Customer {
    /** @no-named-arguments */
    public function __construct(public string $name, public int $age) {}
}
function probe(): Customer {
    return new Customer(age: 23, name: 'Ada');
}
