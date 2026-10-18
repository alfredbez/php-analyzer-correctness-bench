<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(optionalText(null) === null);
check(optionalText(new ParentValue(new ChildValue())) === 'child');
