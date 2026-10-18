<?php
declare(strict_types=1);

/** @template T */
final class EqualValue {
    /** @param T $value */
    public function __construct(private mixed $value) {}
    /** @return T */
    public function checked(mixed $input): mixed {
        if ($input !== $this->value) { throw new InvalidArgumentException(); }
        return $input;
    }
}
function equalInt(mixed $input): int { return (new EqualValue(7))->checked($input); }
