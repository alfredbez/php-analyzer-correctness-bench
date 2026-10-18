<?php

declare(strict_types=1);

// Runtime side of the ground truth: Exception is in RuntimeException's parent
// chain, and instanceof follows the chain, so the check is true for an instance
// and for an instance of a subclass.

require __DIR__ . '/../src/repro.php';

use function Bench\Narrowing\RedundantInstanceofOnDeclaredClass\is_exception;

$parents = class_parents(\RuntimeException::class) ?: [];

if (!in_array(\Exception::class, $parents, true)) {
    fwrite(STDERR, sprintf("Exception is not a parent of RuntimeException: %s\n",
        $parents === [] ? 'none' : implode(', ', $parents)));
    exit(1);
}

class SpecificRuntimeException extends \RuntimeException {}

foreach ([new \RuntimeException('x'), new SpecificRuntimeException('y')] as $e) {
    if ($e instanceof \Exception !== true) {
        fwrite(STDERR, sprintf("%s is not an Exception\n", get_class($e)));
        exit(1);
    }
    if (is_exception($e) !== true) {
        fwrite(STDERR, sprintf("is_exception(%s) is not true\n", get_class($e)));
        exit(1);
    }
}

printf("RuntimeException's parents are %s; is_exception() held for 2 instance(s)\n",
    implode(', ', $parents));
exit(0);
