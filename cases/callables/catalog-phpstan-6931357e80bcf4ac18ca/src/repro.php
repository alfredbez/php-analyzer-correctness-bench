<?php
declare(strict_types=1);

function immediate(int $number): int { return (fn($value): int => $value)($number); }
