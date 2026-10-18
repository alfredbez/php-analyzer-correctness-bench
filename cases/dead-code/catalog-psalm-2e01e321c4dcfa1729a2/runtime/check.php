<?php
require __DIR__ . '/../src/probe.php';
$object = (object)['a' => 42];
if (probe($object) !== $object) { exit(1); }
$object->a = 43;
if (probe($object)->a !== 43) { exit(2); }
if (!is_object((object)42)) { exit(3); }
