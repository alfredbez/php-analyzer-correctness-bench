<?php

declare(strict_types=1);

// Runtime side of the ground truth. A docblock element type is not enforced by
// PHP: an array that the caller declares as array<int, scalar> may hold a float,
// and the callee that declares array<string> treats every element as a string.
// The callee therefore breaks on a legal value of the argument's declared type,
// which is what makes the call - not the docblock - the thing under test.

require __DIR__ . '/../src/repro.php';

use function Bench\Arrays\ScalarArrayForStringArray\load;
use function Bench\Arrays\ScalarArrayForStringArray\total_length;

// The happy path: a genuinely string-valued array is accepted and counted.
if (total_length(['a', 'bc']) !== 3) {
    fwrite(STDERR, "total_length(['a', 'bc']) did not return 3\n");
    exit(1);
}

// The argument the fixture passes really does carry a non-string element, so
// the declared element type array<int, scalar> is not a promise of strings.
$values = load();

$non_string = array_filter($values, static fn ($value): bool => !is_string($value));
if ($non_string === []) {
    fwrite(STDERR, "the argument contains only strings; the case is not exercised\n");
    exit(1);
}

// PHP does not check docblock element types, so the call is accepted by the
// runtime and fails inside the callee instead: strlen() receives a float.
$type_error = null;
try {
    total_length($values);
} catch (TypeError $error) {
    $type_error = $error;
}

if ($type_error === null) {
    fwrite(STDERR, "total_length() accepted a float element; the declared element type is not load-bearing\n");
    exit(1);
}

if (strpos($type_error->getMessage(), 'strlen') === false
    || strpos($type_error->getMessage(), 'string') === false) {
    fwrite(STDERR, sprintf("unexpected failure inside the callee: %s\n", $type_error->getMessage()));
    exit(1);
}

printf(
    "array<int, scalar> argument carries %d non-string element(s); the array<string> callee fails: %s\n",
    count($non_string),
    $type_error->getMessage()
);
exit(0);
