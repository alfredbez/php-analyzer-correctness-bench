<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use Bench\Assignability\StaticPrivatePropertyAccess\BaseCounter;
use Bench\Assignability\StaticPrivatePropertyAccess\SubCounter;

if (BaseCounter::readCount() !== 1) {
    fwrite(STDERR, "Expected BaseCounter::readCount() to return 1\n");
    exit(1);
}

if (SubCounter::readSubCount() !== 2) {
    fwrite(STDERR, "Expected SubCounter::readSubCount() to return 2\n");
    exit(1);
}

try {
    SubCounter::readCount();
    fwrite(STDERR, "Expected Error when calling SubCounter::readCount()\n");
    exit(1);
} catch (\Error $error) {
    if (strpos($error->getMessage(), 'Cannot access private property') === false) {
        fwrite(STDERR, sprintf("Unexpected Error: %s\n", $error->getMessage()));
        exit(1);
    }
}

echo "static::\$privateProperty throws Error on subclass access\n";
exit(0);
