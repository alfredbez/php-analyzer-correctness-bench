<?php

declare(strict_types=1);

// Runtime side of the ground truth. array_filter() keeps the original keys, so
// removing an earlier element while keeping a later one leaves a hole. The
// fixture therefore can hand a non-list to a function documented as
// taking list<int>. A docblock type is not enforced, so the call itself does not
// throw - that is why the proof demonstrates the key handling the expectation
// rests on instead of an exception.

require __DIR__ . '/../src/repro.php';

use function Bench\LegacyPatterns\ArrayFilterStringCallableLosesList\only_ints;

$rows = ['first', 1];

// The fixture runs without a TypeError although the callee documents list<int>.
only_ints($rows);

$filtered = array_filter($rows, 'is_int');

if ($filtered !== [1 => 1]) {
    fwrite(STDERR, sprintf("unexpected filter result: %s\n", var_export($filtered, true)));
    exit(1);
}

if (array_is_list($filtered)) {
    fwrite(STDERR, "array_filter() reindexed the result; the keys were not preserved\n");
    exit(1);
}

printf("array_filter() kept key 1 and produced a non-list: %s\n", var_export($filtered, true));
exit(0);
