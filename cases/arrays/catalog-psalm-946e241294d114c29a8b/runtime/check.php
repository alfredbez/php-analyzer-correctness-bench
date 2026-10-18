<?php
require __DIR__ . '/../src/fixture.php';
if (replace() !== [0, 1]) { throw new RuntimeException('by-reference variable replacement'); }
