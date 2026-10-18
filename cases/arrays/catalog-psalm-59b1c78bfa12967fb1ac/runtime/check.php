<?php
require __DIR__ . '/../src/probe.php';
$sorted = probe(['b' => ['y' => 2], 'a' => ['y' => 1]]);
if (array_keys($sorted) !== ['a', 'b']) { exit(1); }
try { probe(['a' => ['width' => 3]]); exit(2); } catch (ValueError $e) {}
