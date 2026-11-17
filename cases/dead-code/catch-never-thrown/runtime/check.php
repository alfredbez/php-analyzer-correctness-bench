<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use function Bench\DeadCode\CatchNeverThrown\doubleValue;

if (doubleValue(4) !== 8 || doubleValue(0) !== 0) {
    fwrite(STDERR, "Unexpected doubleValue() result\n");
    exit(1);
}

echo "try block executes without ever throwing UnusedDomainException\n";
exit(0);
