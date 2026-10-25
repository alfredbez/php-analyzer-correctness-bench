<?php
declare(strict_types=1);

function invert_boolean(bool $value): mixed {
    return ~$value;
}

function invert_bits(int|string $value): int|string {
    return ~$value;
}
