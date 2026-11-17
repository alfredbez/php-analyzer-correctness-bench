<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use function Bench\Arrays\UninitializedArrayOffsetAutovivification\buildPagination;

set_error_handler(static function (int $severity, string $message): bool {
    throw new \ErrorException($message, 0, $severity);
});

$clamped = buildPagination(20, 250);
if ($clamped !== ['offset' => 20, 'limit' => 100]) {
    fwrite(STDERR, sprintf("Unexpected clamped result: %s\n", var_export($clamped, true)));
    exit(1);
}

$kept = buildPagination(0, 25);
if ($kept !== ['offset' => 0, 'limit' => 25]) {
    fwrite(STDERR, sprintf("Unexpected kept result: %s\n", var_export($kept, true)));
    exit(1);
}

echo "Array offset assignment autovivifies uninitialized local variable without warnings\n";
exit(0);
