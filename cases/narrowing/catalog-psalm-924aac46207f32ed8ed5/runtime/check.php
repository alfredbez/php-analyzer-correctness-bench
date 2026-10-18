<?php
require __DIR__ . '/../src/fixture.php';
foreach ([1, 2, PHP_INT_MAX] as $value) { if (positive($value) !== $value) { throw new RuntimeException('identity cast'); } }
