<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
$receiver = new Receiver(); $yes = bound($receiver); check($yes instanceof Closure); check($yes() === $receiver);
$no = bound(null); check($no instanceof Closure); check($no() === null);
