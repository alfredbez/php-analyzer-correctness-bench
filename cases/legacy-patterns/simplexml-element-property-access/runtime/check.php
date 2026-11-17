<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use function Bench\LegacyPatterns\SimpleXmlElementPropertyAccess\readBookTitle;

set_error_handler(static function (int $severity, string $message): bool {
    throw new \ErrorException($message, 0, $severity);
});

$withTitle = new \SimpleXMLElement('<book><title>Dune</title></book>');
$title = readBookTitle($withTitle);
if ($title !== 'Dune') {
    fwrite(STDERR, sprintf("Expected 'Dune', got %s\n", var_export($title, true)));
    exit(1);
}

$withoutTitle = new \SimpleXMLElement('<book></book>');
$missing = readBookTitle($withoutTitle);
if ($missing !== null) {
    fwrite(STDERR, sprintf("Expected null, got %s\n", var_export($missing, true)));
    exit(1);
}

echo "SimpleXMLElement property access works at runtime\n";
exit(0);
