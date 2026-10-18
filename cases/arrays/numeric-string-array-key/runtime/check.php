<?php

declare(strict_types=1);

// Runtime side of the ground truth. PHP normalises an array key that is a
// canonical decimal integer string to int, so key '10' and key 10 address the
// same element and array_key_exists('10', ...) is true for an array with key
// 10. A docblock type is not enforced, so the fixture's guards decide: nothing
// throws and the guarded reads are the only reads.

require __DIR__ . '/../src/repro.php';

use function Bench\Arrays\NumericStringArrayKey\fetch;

$data = [10 => 'kept'];

if (array_keys($data) !== [10]) {
    fwrite(STDERR, sprintf("key normalisation changed: %s\n", var_export(array_keys($data), true)));
    exit(1);
}

if (!array_key_exists('10', $data)) {
    fwrite(STDERR, "array_key_exists('10', ...) is false although key 10 is set\n");
    exit(1);
}

if (!isset($data['10'])) {
    fwrite(STDERR, "isset(\$data['10']) is false although key 10 is set\n");
    exit(1);
}

if ($data['10'] !== 'kept') {
    fwrite(STDERR, "the string offset did not reach the int key\n");
    exit(1);
}

// A write through one spelling is visible through the other: one slot, not two.
$data['10'] = 'written';

if ($data[10] !== 'written') {
    fwrite(STDERR, "writing \$data['10'] did not update key 10\n");
    exit(1);
}

// Asymmetric control: only canonical decimal integer strings are cast. Typical
// near misses stay strings and are different keys from any int.
$other = ['10x' => 'a', ' 10' => 'b', '+10' => 'c', '1.0' => 'd'];

foreach (array_keys($other) as $key) {
    if (!is_string($key)) {
        fwrite(STDERR, sprintf("non-canonical key %s was cast to int\n", var_export($key, true)));
        exit(1);
    }
}

if (array_key_exists('10', $other)) {
    fwrite(STDERR, "a non-canonical '10'-like key was folded onto int 10\n");
    exit(1);
}

// The fixture itself runs: neither guard throws, and both accepted reads are
// 'kept' -> the two call sites the case is about are exercised.
fetch([10 => 'kept']);

printf("key 10 is reachable as '10' (array_key_exists, isset, read, write); %d near miss(es) stayed strings\n", count($other));
exit(0);
