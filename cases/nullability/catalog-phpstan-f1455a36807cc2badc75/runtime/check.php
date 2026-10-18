<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(itemName(new ItemHolder(new Item())) === 'kept');
check(itemName(new ItemHolder(null)) === null);
