<?php

declare(strict_types=1);

// Runtime side of the ground truth: the branch is never entered for string
// values. The sample is not exhaustive - the argument for exhaustiveness is the
// language reference (is_int() returns false for every non-int) - but a
// demonstration that the code path is dead is stronger evidence than a claim.

require __DIR__ . '/../src/repro.php';

use function Bench\Narrowing\IsIntOnString\classify;

$samples = ['', '0', 'abc', '123', '1e3', ' 12 '];

foreach ($samples as $sample) {
    if (classify($sample) !== 'string') {
        fwrite(STDERR, sprintf("unreachable branch entered for %s\n", var_export($sample, true)));
        exit(1);
    }
}

printf("classify() stayed on the string path for %d sample value(s)\n", count($samples));
exit(0);
