<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
check(upperKeys(['foo' => 9, 2 => 'keep']) === ['FOO' => 9, 2 => 'keep']);
check(array_change_key_case(['Foo' => 1, 'FOO' => 2], CASE_UPPER) === ['FOO' => 2]);
