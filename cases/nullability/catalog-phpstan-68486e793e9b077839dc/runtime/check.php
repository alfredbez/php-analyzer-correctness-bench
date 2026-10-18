<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(size(null) === 0); check(size(['a','b']) === 2);
try { count(null); check(false); } catch (TypeError) {}
