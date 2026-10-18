<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(knownDate()->format('Y-m-d') === '2020-10-12');
check(date_create_immutable('202/20') === false);
