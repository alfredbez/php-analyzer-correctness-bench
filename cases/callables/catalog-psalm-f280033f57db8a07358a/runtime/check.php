<?php
require __DIR__ . '/../src/fixture.php';
if (!(malformed() instanceof Closure) || !(control() instanceof Closure)) { throw new RuntimeException('docblock erasure'); }
malformed()();
control()();
