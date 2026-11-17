<?php

declare(strict_types=1);

namespace Bench\PhpdocExtensions\ParamTagMissingVariable;

/**
 * @param string[]
 */
function countLabels(array $labels): int
{
    return count($labels);
}

/**
 * @param string[] $labels
 */
function countValidLabels(array $labels): int
{
    return count($labels);
}
