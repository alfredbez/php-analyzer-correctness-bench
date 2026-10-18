<?php
declare(strict_types=1);

/** @property-read int $number */
final class MagicNumber {
    public function __get(string $name): int { return strlen($name); }
}
function magicNumber(MagicNumber $value): int { return $value->number; }
