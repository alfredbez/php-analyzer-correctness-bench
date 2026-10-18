<?php

declare(strict_types=1);

namespace Bench\LegacyPatterns\ArrayFilterStringCallableLosesList;

/**
 * @param list<int> $_
 */
function accept_list_of_ints(array $_): void {}

/**
 * Legacy code filters with a string callable and then treats the result as a
 * list. array_filter() keeps the original keys, so removing an earlier element
 * while retaining a later one leaves a hole and the result is not a list.
 *
 * @param list<mixed> $rows
 */
function only_ints(array $rows): void
{
    $filtered = array_filter($rows, 'is_int');
    accept_list_of_ints($filtered);
}
