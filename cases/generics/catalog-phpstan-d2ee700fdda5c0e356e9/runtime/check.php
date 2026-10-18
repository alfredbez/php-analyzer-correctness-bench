<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(equalInt(7) === 7);
try { equalInt('7'); check(false); } catch (InvalidArgumentException) {}
