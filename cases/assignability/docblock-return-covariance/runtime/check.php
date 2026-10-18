<?php

declare(strict_types=1);

// Runtime side of the ground truth. Shelter documents adopt() as returning
// Dog; BadShelter overrides it and documents Animal, returning a Cat. PHP
// enforces only the native signature (Animal -> Animal is legal), so the
// widening is silent until a caller that believes the parent's contract calls a
// Dog-only method.

require __DIR__ . '/../src/repro.php';

use Bench\Assignability\DocblockReturnCovariance\BadShelter;
use Bench\Assignability\DocblockReturnCovariance\Cat;
use Bench\Assignability\DocblockReturnCovariance\Dog;
use Bench\Assignability\DocblockReturnCovariance\Shelter;
use function Bench\Assignability\DocblockReturnCovariance\wake;

if (!(new Shelter())->adopt() instanceof Dog) {
    fwrite(STDERR, "Shelter::adopt() does not return a Dog; the parent promise is wrong\n");
    exit(1);
}

// The parent contract holds, so wake() works against the parent.
if (wake(new Shelter()) !== 'woof') {
    fwrite(STDERR, "wake(new Shelter()) did not return 'woof'\n");
    exit(1);
}

$widened = (new BadShelter())->adopt();

if (!$widened instanceof Cat) {
    fwrite(STDERR, "BadShelter::adopt() did not return a Cat\n");
    exit(1);
}

// The consequence the case is about: a caller that trusts the parent's
// documented return type crashes on the widened override.
try {
    wake(new BadShelter());
} catch (Error $error) {
    if (strpos($error->getMessage(), 'bark') === false) {
        fwrite(STDERR, sprintf("unexpected Error: %s\n", $error->getMessage()));
        exit(1);
    }

    printf("BadShelter::adopt() returns a Cat, so wake() throws: %s\n", $error->getMessage());
    exit(0);
}

fwrite(STDERR, "wake(new BadShelter()) returned; the widened override did not break the caller\n");
exit(1);
