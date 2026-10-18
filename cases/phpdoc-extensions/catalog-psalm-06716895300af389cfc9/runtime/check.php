<?php
require __DIR__ . '/../src/probe.php';
if (!(Left::probe(0) instanceof Left) || !(Left::probe(1) instanceof Right) || Left::probe(2) !== null) { exit(1); }
