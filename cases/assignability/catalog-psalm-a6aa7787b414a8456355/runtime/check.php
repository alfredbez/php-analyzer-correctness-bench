<?php
require __DIR__ . '/../src/fixture.php';
try { LocalFailure::fail(); } catch (LocalFailure $e) { if ($e->getMessage() === 'local') { exit(0); } }
throw new RuntimeException('self exception');
