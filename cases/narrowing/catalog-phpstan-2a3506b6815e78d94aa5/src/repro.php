<?php
declare(strict_types=1);

/** @param mixed $value */
function assertBoolean($value, bool $wanted): void {
    if ($value !== $wanted) { throw new InvalidArgumentException(); }
}
function checked(mixed $value, bool $wanted): bool {
    assertBoolean($value, $wanted);
    return $value;
}
