<?php
declare(strict_types=1);

/** @implements ArrayAccess<int, int> */
final class IntOffsets implements ArrayAccess {
    #[Override]
    public function offsetExists(mixed $offset): bool { return $offset === 0; }
    #[Override]
    public function offsetGet(mixed $offset): int { return $offset === 0 ? 7 : 0; }
    #[Override]
    public function offsetSet(mixed $offset, mixed $value): void {}
    #[Override]
    public function offsetUnset(mixed $offset): void {}
}
function offsetValue(IntOffsets $values): int { return $values[0]; }
