<?php
declare(strict_types=1);

final class Receiver { public int $number = 7; }
function bound(?Receiver $receiver): ?Closure {
    return Closure::bind(function (): ?object { return isset($this) ? $this : null; }, $receiver);
}
