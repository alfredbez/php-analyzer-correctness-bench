<?php
require __DIR__ . '/../src/probe.php';
// PHP ignores the malformed comment; this does not prove alias-parser behavior.
if (!(new First() instanceof First) || !(new Second() instanceof Second)) { exit(1); }
