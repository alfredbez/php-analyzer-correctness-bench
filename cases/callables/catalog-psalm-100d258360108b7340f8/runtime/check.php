<?php
require __DIR__ . '/../src/probe.php';
if (probe() !== 'hello reader') { exit(1); }
$method = new ReflectionMethod(Greeter::class, 'greet');
if ($method->invoke(null) !== 'hello world') { exit(2); }
