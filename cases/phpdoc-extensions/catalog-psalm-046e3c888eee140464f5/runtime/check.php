<?php
require __DIR__ . '/../src/probe.php';
if (probe(false) !== 7) { exit(1); }
try { probe(true); exit(2); } catch (InvalidArgumentException $e) {}
