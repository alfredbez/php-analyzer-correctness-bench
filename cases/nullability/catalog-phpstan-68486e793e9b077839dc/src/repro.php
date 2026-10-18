<?php
declare(strict_types=1);

/** @param string[] $values */
function size(?array $values): int {
    if ($values === null) { return 0; }
    return count($values);
}
