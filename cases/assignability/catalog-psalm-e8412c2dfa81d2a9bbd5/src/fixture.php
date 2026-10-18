<?php
declare(strict_types=1);
function add(int $a, int $b, int $c): int { return $a + $b + $c; }
function unpacked(): int { return add(1, ...[2, 3]); }
function control(): int { return add(1, 2, 3); }
