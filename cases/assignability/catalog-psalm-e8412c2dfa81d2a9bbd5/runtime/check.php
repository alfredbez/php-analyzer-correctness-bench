<?php
require __DIR__ . '/../src/fixture.php';
if (unpacked() !== 6 || unpacked() !== control()) { throw new RuntimeException('literal unpack'); }
