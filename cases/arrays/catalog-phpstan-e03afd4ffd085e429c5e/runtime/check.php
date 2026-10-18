<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(offsetValue(new IntOffsets()) === 7);
$value = new IntOffsets(); check($value[1] === 0); check(isset($value[0]) && !isset($value[1]));
