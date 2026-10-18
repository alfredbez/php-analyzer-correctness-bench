<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(fill(['a' => null, 'b' => 'kept']) === ['a' => 'CONTENT', 'b' => 'KEPT']);
check(fill([]) === []);
