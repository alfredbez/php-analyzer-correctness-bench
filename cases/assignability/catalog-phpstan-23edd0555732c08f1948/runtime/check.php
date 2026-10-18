<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(documented(5) === 5);
try { documented('bad'); check(false); } catch (TypeError) {}
