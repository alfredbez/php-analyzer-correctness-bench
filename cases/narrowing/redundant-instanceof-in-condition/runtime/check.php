<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use function Bench\Narrowing\RedundantInstanceofInCondition\is_exception;

if (!is_subclass_of(\RuntimeException::class, \Exception::class)) {
    throw new \RuntimeException('RuntimeException must extend Exception');
}

class ChildException extends \RuntimeException {}

foreach ([new \RuntimeException('parent'), new ChildException('child')] as $value) {
    if (is_exception($value) !== true) {
        throw new \RuntimeException('The ancestor check took the false branch');
    }
}

echo "The ancestor check takes the true branch for the declared class and a subclass\n";
