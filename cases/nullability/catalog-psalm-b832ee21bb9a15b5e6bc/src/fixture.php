<?php
declare(strict_types=1);
class Item { public function value(): int { return 7; } }
function maybe(bool $present): ?Item { return $present ? new Item() : null; }
function unsafe(bool $present): int { return maybe($present)->value(); }
function safe(bool $present): ?int { return maybe($present)?->value(); }
