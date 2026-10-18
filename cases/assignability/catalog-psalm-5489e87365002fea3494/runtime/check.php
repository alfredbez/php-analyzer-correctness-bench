<?php
require __DIR__ . '/../src/probe.php';
foreach (['0', 'x', ' '] as $left) {
    foreach (['0', 'y', ' '] as $right) {
        if (!probe($left, $right) || strlen(probe($left, $right)) < 2) { exit(1); }
    }
}
if ((bool)'0' !== false || (bool)'' !== false) { exit(2); }
