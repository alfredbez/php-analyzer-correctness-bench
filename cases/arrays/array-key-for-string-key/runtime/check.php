<?php

declare(strict_types=1);

// Runtime side of the ground truth. An array key is an int or a string and
// nothing else, so a caller whose array is typed array<array-key, int> may hand
// the callee an int key. The callee declares array<string, int> and uses every
// key as a string, so the call is the thing under test: the argument is legal
// PHP and the callee still fails on it.

require __DIR__ . '/../src/repro.php';

use function Bench\Arrays\ArrayKeyForStringKey\load;
use function Bench\Arrays\ArrayKeyForStringKey\render;

// The happy path: an all-string-keyed array renders.
if (render(['users' => 2]) !== 'USERS:2;') {
    fwrite(STDERR, "render(['users' => 2]) did not render 'USERS:2;'\n");
    exit(1);
}

// The argument's key set is a subset of array-key and really contains an int.
$counts = load();
$keys = array_keys($counts);

if (array_filter($keys, 'is_int') === []) {
    fwrite(STDERR, "the argument has no int key; the case is not exercised\n");
    exit(1);
}

foreach ($keys as $key) {
    if (!is_int($key) && !is_string($key)) {
        fwrite(STDERR, sprintf("unexpected key type %s\n", get_debug_type($key)));
        exit(1);
    }
}

// PHP does not check docblock key types either, so the call is accepted and the
// callee fails: strtoupper() receives the int key.
$type_error = null;
try {
    render([0 => 1]);
} catch (TypeError $error) {
    $type_error = $error;
}

if ($type_error === null) {
    fwrite(STDERR, "render() accepted an int key; the declared key type is not load-bearing\n");
    exit(1);
}

if (strpos($type_error->getMessage(), 'strtoupper') === false
    || strpos($type_error->getMessage(), 'string') === false) {
    fwrite(STDERR, sprintf("unexpected failure inside the callee: %s\n", $type_error->getMessage()));
    exit(1);
}

// Asymmetric control: a numeric string key does not survive as a string, so a
// callee cannot make its array<string> promise true by spelling the key as a
// string either.
$numeric = ['10' => 1];
if (array_keys($numeric) !== [10]) {
    fwrite(STDERR, sprintf("key normalisation changed: %s\n", var_export(array_keys($numeric), true)));
    exit(1);
}

printf(
    "array<array-key, int> argument keys include int 0; the array<string, int> callee fails: %s\n",
    $type_error->getMessage()
);
exit(0);
