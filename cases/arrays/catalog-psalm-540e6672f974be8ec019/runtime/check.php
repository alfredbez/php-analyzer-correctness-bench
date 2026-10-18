<?php
require __DIR__ . '/../src/probe.php';
if (probe([2, 3]) !== 5) { exit(1); }
try { probe(new stdClass()); exit(2); } catch (Error $e) {
    if (!str_contains($e->getMessage(), 'unpack')) { exit(3); }
}
try { probe(new ArrayIterator([])); exit(4); } catch (ArgumentCountError $e) {}
