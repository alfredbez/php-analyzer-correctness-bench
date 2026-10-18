<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(readSlot() === 7);
check(keyed('other') === ['other' => 7]);
check(!array_key_exists('TKey', keyed('slot')));
