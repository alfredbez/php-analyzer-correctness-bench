<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(firstOnly(Choice::First) === Choice::First);
check(firstOnly(Choice::Second) === null); check(firstOnly(Choice::Third) === null);
