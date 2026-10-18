<?php
require __DIR__ . '/../src/fixture.php';
$object = new stdClass();
if (nullValue() !== null || accept($object) !== $object || accept('x') !== 'x') { throw new RuntimeException('nullable object union'); }
