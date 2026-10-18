<?php
require __DIR__ . '/../src/fixture.php';
if (maybe(false) !== null || !(maybe(true) instanceof stdClass) || guarded(false) || !guarded(true)) { throw new RuntimeException('native nullable return'); }
