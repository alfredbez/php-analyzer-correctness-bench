<?php

declare(strict_types=1);

// Runtime side of the ground truth. A `finally` block always runs, including
// while an exception is unwinding towards an outer `catch`, so the flag the
// ternary reads is true. The sample is single-valued because the function takes
// no input and has no branches other than the one under test.

require __DIR__ . '/../src/repro.php';

use function Bench\DeadCode\FinallyAssignment\cleaned_flag;

$result = cleaned_flag();

if ($result !== 1) {
    fwrite(STDERR, sprintf("cleaned_flag() returned %s, the finally block did not run first\n", var_export($result, true)));
    exit(1);
}

printf("the finally assignment ran before the catch: cleaned_flag() === %d\n", $result);
exit(0);
