<?php
require __DIR__ . '/../src/fixture.php';
$domain = ['red', 'blue', 1, 2, 3];
if (in_array(bad(), $domain, true) || !in_array(good(), $domain, true)) { throw new RuntimeException('literal membership'); }
