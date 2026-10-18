<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(firstOrText(new FirstValue([7])) === 7);
check(firstOrText(new FirstValue([])) === 'empty');
check((new FirstValue([]))->first() === null);
