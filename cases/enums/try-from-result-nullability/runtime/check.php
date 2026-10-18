<?php

declare(strict_types=1);

// Runtime side of the ground truth. BackedEnum::tryFrom() returns the case for
// a known backing value and null otherwise, while from() throws ValueError
// instead - the two are not interchangeable, and only tryFrom()'s result is
// nullable.

require __DIR__ . '/../src/repro.php';

use Bench\Enums\TryFromResultNullability\Status;
use function Bench\Enums\TryFromResultNullability\label_of_known;
use function Bench\Enums\TryFromResultNullability\label_of_unknown;

// The literal that reaches tryFrom() in the fixture is a valid backing value,
// so the result is the case, never null. label_of_known() is the call the case
// says no diagnostic may be attached to.
if (Status::tryFrom('active') !== Status::Active) {
    fwrite(STDERR, "tryFrom('active') did not return the Active case\n");
    exit(1);
}

if (label_of_known() !== 'active') {
    fwrite(STDERR, "label_of_known() did not return 'active'\n");
    exit(1);
}

if (label_of_unknown('active') !== 'active') {
    fwrite(STDERR, "the variable-input wrapper rejected a valid backing value\n");
    exit(1);
}

// The nullable path is real: an unknown value yields null and label() rejects
// it with a TypeError.
if (Status::tryFrom('nope') !== null) {
    fwrite(STDERR, "tryFrom('nope') did not return null\n");
    exit(1);
}

try {
    label_of_unknown('nope');
    fwrite(STDERR, "label(null) did not throw; the nullable path is not rejected\n");
    exit(1);
} catch (TypeError $error) {
    // expected: null is not a Status
}

// Asymmetric control: from() is not nullable, it throws ValueError.
try {
    Status::from('nope');
    fwrite(STDERR, "from('nope') did not throw a ValueError\n");
    exit(1);
} catch (ValueError $error) {
    printf("tryFrom('active') = Status::Active, tryFrom('nope') = null and label(null) is a TypeError; from('nope') throws ValueError instead\n");
    exit(0);
}
