<?php
declare(strict_types=1);
/** @throws \Exception| \InvalidArgumentException */
function probe(bool $fail): int {
    if ($fail) { throw new InvalidArgumentException('negative control'); }
    return 7;
}
