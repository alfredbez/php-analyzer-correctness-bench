<?php

declare(strict_types=1);

// Runtime side of the ground truth. The bound, not a docblock, decides the
// violation: \Countable is a real interface and instanceof answers it for the
// value the fixture passes. The fixture's body itself is fine - count() accepts
// arrays - so no exception marks the breach; the breach is the value not
// satisfying the bound the function declares.

require __DIR__ . '/../src/repro.php';

use function Bench\Generics\TemplateBoundViolation\count_object;
use function Bench\Generics\TemplateBoundViolation\count_three;

$tuple = [1, 2, 3];

if ($tuple instanceof Countable) {
    fwrite(STDERR, "an array is Countable; the bound would be satisfied\n");
    exit(1);
}

if ($tuple instanceof Traversable) {
    fwrite(STDERR, "an array is Traversable; the bound would be satisfied\n");
    exit(1);
}

$countable = new ArrayObject($tuple);

if (!$countable instanceof Countable) {
    fwrite(STDERR, "ArrayObject is not Countable; the control is not a valid bound\n");
    exit(1);
}

if (count_object() !== 3) {
    fwrite(STDERR, "the bound-satisfying control did not work\n");
    exit(1);
}

// The argument the case rejects still runs here: count([1,2,3]) is legal, which
// is why only an analyzer can catch it - the runtime cannot.
if (count_three() !== 3) {
    fwrite(STDERR, sprintf("count_three() returned %s\n", var_export(count_three(), true)));
    exit(1);
}

printf("[1,2,3] instanceof Countable is false while count_all([1,2,3]) = 3: the bound is violated, not the body\n");
exit(0);
