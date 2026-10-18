<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(remaining(new Exception('x')) === null);
$error = new TypeError('x'); check(remaining($error) === $error);
