<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use function Bench\PhpdocExtensions\ParamTagMissingVariable\countLabels;
use function Bench\PhpdocExtensions\ParamTagMissingVariable\countValidLabels;

if (countLabels(['a', 'b']) !== 2) {
    fwrite(STDERR, "Expected countLabels(['a', 'b']) === 2\n");
    exit(1);
}

if (countValidLabels(['x']) !== 1) {
    fwrite(STDERR, "Expected countValidLabels(['x']) === 1\n");
    exit(1);
}

echo "PHPDoc comments are ignored at runtime\n";
exit(0);
