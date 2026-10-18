<?php
require __DIR__ . '/../src/probe.php';
if (Routes::probe(['rule' => 'home']) !== 'home' || Routes::probe(['rule' => 'next', 'middleware' => [Exception::class => ['auth']]]) !== 'next') { exit(1); }
