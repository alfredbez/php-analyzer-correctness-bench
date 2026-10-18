<?php
require __DIR__ . '/../src/probe.php';
if (!probe([2 => 1], [], [2]) || probe([], [], [2]) || probe([2 => 1], [2 => 1], [2])) { exit(1); }
try { probe([], [], [[1]]); exit(2); } catch (TypeError $e) {}
