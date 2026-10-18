<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(consume(new IntValue()) === 7);
try { (static fn(int $x): int => $x)('bad'); check(false); } catch (TypeError) {}
