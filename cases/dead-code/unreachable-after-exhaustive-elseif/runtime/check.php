<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use function Bench\DeadCode\UnreachableAfterExhaustiveElseif\classifyFlag;

if (classifyFlag(true) !== 1) {
    fwrite(STDERR, "Expected classifyFlag(true) === 1\n");
    exit(1);
}

if (classifyFlag(false) !== 2) {
    fwrite(STDERR, "Expected classifyFlag(false) === 2\n");
    exit(1);
}

echo "Exhaustive if/elseif branches terminate for every bool input\n";
exit(0);
