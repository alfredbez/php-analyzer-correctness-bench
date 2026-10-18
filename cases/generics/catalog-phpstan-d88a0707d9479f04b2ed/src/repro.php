<?php
declare(strict_types=1);

/** @template T */
final class FirstValue {
    /** @param list<T> $items */
    public function __construct(private array $items) {}
    /**
     * @template D
     * @param D $default
     * @return T|D
     */
    public function first(mixed $default = null): mixed { return $this->items[0] ?? $default; }
}
/** @param FirstValue<int> $values */
function firstOrText(FirstValue $values): int|string { return $values->first('empty'); }
