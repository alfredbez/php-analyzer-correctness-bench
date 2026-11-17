<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use Bench\Assignability\DocblockParameterContravariance\Constraint;
use Bench\Assignability\DocblockParameterContravariance\LengthConstraint;
use Bench\Assignability\DocblockParameterContravariance\LengthValidator;
use function Bench\Assignability\DocblockParameterContravariance\check;

if (check(new LengthValidator(), 'hello', new LengthConstraint()) !== true) {
    fwrite(STDERR, "Expected 'hello' to pass LengthValidator\n");
    exit(1);
}

if (check(new LengthValidator(), 'hi', new LengthConstraint()) !== false) {
    fwrite(STDERR, "Expected 'hi' to fail LengthValidator\n");
    exit(1);
}

try {
    check(new LengthValidator(), 123, new LengthConstraint());
    fwrite(STDERR, "Expected TypeError when passing int to narrowed @param string\n");
    exit(1);
} catch (\TypeError $error) {
    if (strpos($error->getMessage(), 'strlen') === false) {
        fwrite(STDERR, sprintf("Unexpected TypeError: %s\n", $error->getMessage()));
        exit(1);
    }
}

try {
    check(new LengthValidator(), 'hello', new Constraint());
    fwrite(STDERR, "Expected Error when passing base Constraint to narrowed @param LengthConstraint\n");
    exit(1);
} catch (\Error $error) {
    if (strpos($error->getMessage(), 'minLength') === false) {
        fwrite(STDERR, sprintf("Unexpected Error: %s\n", $error->getMessage()));
        exit(1);
    }
}

echo "Narrowed @param in child override breaks BaseValidator callers at runtime\n";
exit(0);
