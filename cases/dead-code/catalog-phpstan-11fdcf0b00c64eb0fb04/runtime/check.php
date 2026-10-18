<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check((new DynamicRead('left'))->value === 'left');
check((new DynamicRead('right'))->value === 'right');
