<?php
require __DIR__ . '/../src/probe.php';
if (probe() !== 'value' || readRow(['test' => 'other']) !== 'other') { exit(1); }
try { readRow(['test' => []]); exit(2); } catch (TypeError $e) {}
