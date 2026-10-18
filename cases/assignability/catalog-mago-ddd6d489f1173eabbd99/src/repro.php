<?php
declare(strict_types=1);
final class Service {
    public function __construct(public bool $result) {}
    public function execute(): bool { return $this->result; }
}
function service(string $text): ?Service {
    return $text === '' ? null : new Service($text === 'yes');
}
function probe(mixed $value): bool {
    return !is_string($value) || (($value = service($value)) === null) || $value->execute();
}
