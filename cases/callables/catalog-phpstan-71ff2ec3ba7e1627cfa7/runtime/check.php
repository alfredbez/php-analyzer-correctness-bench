<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(contextual() === 4);
try { invokeAll([fn(int $value): int => $value]); check(false); } catch (TypeError) {}
