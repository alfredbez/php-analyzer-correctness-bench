<?php
require __DIR__ . '/../src/fixture.php';
if (invoke(['a' => fn() => ['x' => 2]]) !== ['x' => 2] || invoke(['a' => fn() => null]) !== null) { throw new RuntimeException('closure return'); }
