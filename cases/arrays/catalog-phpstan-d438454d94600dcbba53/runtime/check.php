<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(appendCount(0,0,0) === 1); check(appendCount(1,1,1) === 4);
for ($a=-1; $a<=1; $a++) { for ($b=-1; $b<=1; $b++) { for ($c=0; $c<=2; $c++) { $n=appendCount($a,$b,$c); check($n>=1 && $n<=4); } } }
