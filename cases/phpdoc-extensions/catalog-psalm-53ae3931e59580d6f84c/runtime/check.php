<?php
require __DIR__ . '/../src/probe.php';
$customer = probe();
if ($customer->name !== 'Ada' || $customer->age !== 23 || (new Customer('Bob', 24))->age !== 24) { exit(1); }
