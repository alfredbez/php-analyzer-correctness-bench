<?php

declare(strict_types=1);

// Runtime side of the ground truth. The value has exactly two possible shapes
// and the script decides both of them, so the narrowing claim is not sampled:
// 'strlen' is callable and returns early, [1] is not callable and is the only
// value that reaches accept_array(), whose array parameter PHP enforces.

require __DIR__ . '/../src/repro.php';

use function Bench\Callables\NegatedIsCallableRemovesFunctionName\quacks;

if (!is_callable('strlen')) {
    fwrite(STDERR, "'strlen' is not callable\n");
    exit(1);
}

if (is_callable([1])) {
    fwrite(STDERR, "[1] is callable; the guard would not remove the array\n");
    exit(1);
}

quacks(true);
quacks(false);

echo "the guard removed the function name; [1] reached accept_array() without a TypeError\n";
exit(0);
