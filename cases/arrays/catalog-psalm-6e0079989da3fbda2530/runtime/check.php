<?php
require __DIR__ . '/../src/probe.php';
if (probe(false) !== 2) { exit(1); }
try { probe(true); exit(2); } catch (TypeError $e) {}
