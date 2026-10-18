<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(checked(true, true) === true); check(checked(false, false) === false);
try { checked('1', true); check(false); } catch (InvalidArgumentException) {}
