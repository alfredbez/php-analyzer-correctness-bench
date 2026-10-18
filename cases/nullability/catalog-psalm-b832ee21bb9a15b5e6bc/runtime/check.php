<?php
require __DIR__ . '/../src/fixture.php';
if (unsafe(true) !== 7 || safe(false) !== null || safe(true) !== 7) { throw new RuntimeException('nullable controls'); }
try { unsafe(false); } catch (Error $e) { if (str_contains($e->getMessage(), 'on null')) { exit(0); } throw $e; }
throw new RuntimeException('null dereference did not fail');
