<?php
declare(strict_types=1);
/** @no-named-arguments */
function positional(int $left, int $right): int { return $left - $right; }
function bad(): int { return positional(right: 2, left: 5); }
function good(): int { return positional(5, 2); }
