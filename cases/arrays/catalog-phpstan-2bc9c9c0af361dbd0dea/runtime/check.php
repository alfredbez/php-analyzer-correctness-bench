<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(strings([1, 'keep', 'x' => 2, 'y' => 'yes']) === [1 => 'keep', 'y' => 'yes']);
check(strings([1, 2]) === []);
