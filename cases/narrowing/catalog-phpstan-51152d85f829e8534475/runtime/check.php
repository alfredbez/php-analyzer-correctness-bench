<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(caught(false, true) === false);
check(caught(true, false) === true);
check(caught(false, false) === false);
