<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use function Bench\LegacyPatterns\OutParameterUndefinedVariable\extractCaseId;

set_error_handler(static function (int $severity, string $message): bool {
    throw new \ErrorException($message, 0, $severity);
});

$matched = extractCaseId('Case PP-D-12345 opened');
if ($matched !== 'PP-D-12345') {
    fwrite(STDERR, sprintf("Expected 'PP-D-12345', got %s\n", var_export($matched, true)));
    exit(1);
}

$unmatched = extractCaseId('No case id here');
if ($unmatched !== null) {
    fwrite(STDERR, sprintf("Expected null, got %s\n", var_export($unmatched, true)));
    exit(1);
}

echo "preg_match() out-parameter initializes \$matches without warnings\n";
exit(0);
