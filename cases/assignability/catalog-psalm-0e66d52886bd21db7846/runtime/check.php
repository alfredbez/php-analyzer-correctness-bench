<?php
require __DIR__ . '/../src/probe.php';
foreach (['0', '-1', '1.5', '1e2', ' 2'] as $number) {
    foreach (['0', 'x', ' '] as $suffix) {
        if (!probe($number, $suffix) || !reversed($number, $suffix)) { exit(1); }
    }
}
// A single nonempty numeric string is not necessarily truthy.
if ((bool)'0' !== false) { exit(2); }
