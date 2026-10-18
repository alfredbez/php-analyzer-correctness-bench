<?php
declare(strict_types=1);

/**
 * @param array<int|string, int|string> $input
 * @return array<int|string, string>
 */
function strings(array $input): array { return array_filter($input, static fn($value): bool => is_string($value)); }
