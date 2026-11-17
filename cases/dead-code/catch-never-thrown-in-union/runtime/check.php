<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use function Bench\DeadCode\CatchNeverThrownInUnion\safeLoadCount;

if (safeLoadCount(false) !== 3) {
    fwrite(STDERR, "Expected safeLoadCount(false) === 3\n");
    exit(1);
}

if (safeLoadCount(true) !== 0) {
    fwrite(STDERR, "Expected safeLoadCount(true) === 0\n");
    exit(1);
}

echo "Multi-catch handles MissingItemException while StaleStateException is never thrown\n";
exit(0);
