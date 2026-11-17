<?php

declare(strict_types=1);

namespace Bench\LegacyPatterns\OutParameterUndefinedVariable;

function extractCaseId(string $subject): ?string
{
    if (1 !== preg_match('/(PP-[DR]-[a-zA-Z0-9-]+)/', $subject, $matches)) {
        return null;
    }

    return $matches[1];
}
