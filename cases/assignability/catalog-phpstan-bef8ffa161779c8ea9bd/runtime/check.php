<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
for ($i = -9; $i <= 9; $i++) { check(magnitude($i) >= 0 && magnitude($i) <= 9); }
check(magnitude(-9) === 9 && magnitude(0) === 0);
check(is_float(abs(PHP_INT_MIN)));
