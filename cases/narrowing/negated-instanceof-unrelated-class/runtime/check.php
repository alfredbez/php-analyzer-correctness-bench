<?php

declare(strict_types=1);

// Runtime side of the ground truth. Two arguments, one structural and one
// observational:
//
// * structurally, PHP reports the ancestors of a class explicitly
//   (class_parents() / class_implements()). Beta is in neither list of Alpha,
//   and a class has exactly one parent chain, so no instance of Alpha can
//   satisfy `$x instanceof Beta`.
// * observationally, the function returns true for a direct instance and for
//   an instance of a subclass of Alpha.

require __DIR__ . '/../src/repro.php';

use Bench\Narrowing\NegatedInstanceofUnrelatedClass\Alpha;
use Bench\Narrowing\NegatedInstanceofUnrelatedClass\Beta;

use function Bench\Narrowing\NegatedInstanceofUnrelatedClass\is_not_beta;

$ancestors = array_merge(class_parents(Alpha::class) ?: [], class_implements(Alpha::class) ?: []);

if (in_array(Beta::class, $ancestors, true)) {
    fwrite(STDERR, "Beta is an ancestor of Alpha: the negation is not always true\n");
    exit(1);
}

class AlphaChild extends Alpha {}

foreach ([new Alpha(), new AlphaChild()] as $value) {
    if ($value instanceof Beta) {
        fwrite(STDERR, sprintf("%s is an instance of Beta\n", get_class($value)));
        exit(1);
    }
    if (is_not_beta($value) !== true) {
        fwrite(STDERR, sprintf("is_not_beta(%s) is not true\n", get_class($value)));
        exit(1);
    }
}

printf("Alpha's ancestors (%s) exclude Beta; is_not_beta() held for 2 instance(s)\n",
    $ancestors === [] ? 'none' : implode(', ', $ancestors));
exit(0);
