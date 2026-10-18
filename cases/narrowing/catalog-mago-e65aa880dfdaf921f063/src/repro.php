<?php
declare(strict_types=1);
/** @param Exception|string|list<string> $value */
function probe(Exception|string|array $value): string {
    if (is_array($value)) { return 'array'; }
    elseif (empty($value)) { return 'empty'; }
    if (is_string($value)) { return $value; }
    return 'exception';
}
