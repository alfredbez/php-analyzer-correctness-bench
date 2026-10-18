<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
set_error_handler(static fn() => true);
check(shifted(new DateTimeImmutable('2020-01-01'), '+1 day') === '2020-01-02');
check(shifted(new DateTimeImmutable('2020-01-01'), 'koko') === null);
restore_error_handler();
