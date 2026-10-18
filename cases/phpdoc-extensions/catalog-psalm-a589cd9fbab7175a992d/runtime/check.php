<?php
require __DIR__ . '/../src/fixture.php';
if (good() !== 3 || bad() !== 3) { throw new RuntimeException('PHP itself permits named arguments; annotation is a static policy'); }
