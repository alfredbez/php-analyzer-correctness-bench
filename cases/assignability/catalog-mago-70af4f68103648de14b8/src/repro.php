<?php
declare(strict_types=1);
final class Item {
    public function __construct(public bool $valid) {}
    public function isValid(): bool { return $this->valid; }
}
function convert(string $text): ?Item {
    return $text === '' ? null : new Item($text === 'ok');
}
function probe(string $value): Item {
    if (($value = convert($value)) === null || !$value->isValid()) {
        throw new RuntimeException();
    }
    return $value;
}
