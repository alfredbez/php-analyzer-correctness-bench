<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
$value = new ValueObject(); check(sameObject($value) === $value);
try { sameObject(new stdClass()); check(false); } catch (TypeError) {}
