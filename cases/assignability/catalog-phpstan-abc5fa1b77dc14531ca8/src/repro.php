<?php
declare(strict_types=1);

function distinct(): string {
    $a = new class { public int $value = 7; }; $b = new class { public string $value = 'x'; };
    return str_repeat($b->value, $a->value);
}
