<?php

declare(strict_types=1);

namespace Bench\LegacyPatterns\CountOnIterable;

/**
 * Legacy code counts a collection that is only known to be iterable, because
 * the surrounding code still passes plain arrays around. count() accepts an
 * array or a Countable; a Generator or a bare Traversable is neither, so this
 * throws a TypeError for a Traversable that does not implement Countable.
 *
 * @param iterable<int, string> $rows
 */
function row_count(iterable $rows): int
{
    return count($rows);
}
