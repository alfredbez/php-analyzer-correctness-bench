<?php
require __DIR__ . '/../src/fixture.php';
if (good() !== 'NRI') { throw new RuntimeException('named control'); }
try { bad(); } catch (ArgumentCountError $e) { if (str_contains($e->getMessage(), 'required')) { exit(0); } throw $e; }
throw new RuntimeException('missing argument did not fail');
