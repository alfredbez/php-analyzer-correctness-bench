<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(immediate(7) === 7); check(immediate(-2) === -2);
try { (fn($value): int => $value)('bad'); check(false); } catch (TypeError) {}
