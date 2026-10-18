<?php
require __DIR__ . '/../src/fixture.php';
foreach ([[], [1, 2]] as $values) { if (duplicate($values) !== control($values)) { throw new RuntimeException('docblock erasure'); } }
