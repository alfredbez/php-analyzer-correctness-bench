<?php
declare(strict_types=1);
require __DIR__ . '/../src/probe.php';

$first = new FixedReading(11);
$second = new FixedReading(22);
if ($first->value !== 11 || $second->value !== 22) { exit(1); }
foreach ([11, 33] as $replacement) {
    try {
        $first->replace($replacement);
        exit(2);
    } catch (Error $error) {
        if (!str_contains($error->getMessage(), 'Cannot modify readonly property')) { exit(3); }
    }
    if ($first->value !== 11 || $second->value !== 22) { exit(4); }
}
