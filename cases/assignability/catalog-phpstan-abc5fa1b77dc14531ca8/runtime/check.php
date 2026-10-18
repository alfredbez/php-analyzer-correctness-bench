<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(distinct() === 'xxxxxxx');
$a = new class {}; $b = new class {}; check(get_class($a) !== get_class($b));
