<?php
require __DIR__ . '/../src/fixture.php';
if (narrow('red') !== Color::RED || narrow('blue') !== Color::BLUE) { throw new RuntimeException('backed enum values'); }
try { narrow('green'); } catch (InvalidArgumentException $e) { exit(0); }
throw new RuntimeException('invalid enum value passed guard');
