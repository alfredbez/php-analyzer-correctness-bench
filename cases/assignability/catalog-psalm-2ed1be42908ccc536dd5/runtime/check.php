<?php
declare(strict_types=1);
require __DIR__ . '/../src/probe.php';

if (invert_bits(0) !== -1 || invert_bits(1) !== -2) { exit(1); }
if (invert_bits("\x00\x55") !== "\xff\xaa") { exit(2); }
if (invert_bits('') !== '') { exit(3); }
foreach ([true, false] as $value) {
    try {
        invert_boolean($value);
        exit(4);
    } catch (TypeError $error) {
        if (!str_contains($error->getMessage(), 'Cannot perform bitwise not')) { exit(5); }
    }
}
