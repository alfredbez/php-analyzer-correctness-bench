<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check((new IncludedRead('left'))->value === 'left');
check((new IncludedRead('right'))->value === 'right');
