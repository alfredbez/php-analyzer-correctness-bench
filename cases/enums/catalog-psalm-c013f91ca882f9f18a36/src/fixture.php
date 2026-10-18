<?php
declare(strict_types=1);
enum Color: string { case RED = 'red'; case BLUE = 'blue'; }
/** @param value-of<Color> $value */
function fromValue(string $value): Color { return Color::from($value); }
function narrow(string $value): Color {
    if ($value !== Color::RED->value && $value !== Color::BLUE->value) { throw new InvalidArgumentException(); }
    return fromValue($value);
}
