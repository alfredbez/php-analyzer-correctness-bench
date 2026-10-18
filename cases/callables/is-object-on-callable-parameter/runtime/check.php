<?php

declare(strict_types=1);

// Runtime side of the ground truth: the branch is reachable, which is decided
// by calling it with the two object shapes a callable can have. The control
// shows that a plain callable-string does take the other path, so the true
// result is not a tautology of the fixture.

require __DIR__ . '/../src/repro.php';

use Bench\Callables\IsObjectOnCallableParameter\Handler;

use function Bench\Callables\IsObjectOnCallableParameter\quacks;

$closure = static function (): string {
    return 'closed';
};

$cases = [
    [$closure, true, 'Closure'],
    [new Handler(), true, 'Handler'],
    ['strlen', false, 'callable-string'],
];

foreach ($cases as [$value, $expected, $label]) {
    $actual = quacks($value);
    if ($actual !== $expected) {
        fwrite(STDERR, sprintf("quacks(%s) = %s, expected %s\n", $label,
            var_export($actual, true), var_export($expected, true)));
        exit(1);
    }
    if (!is_callable($value)) {
        fwrite(STDERR, sprintf("%s is not callable, the fixture could not be driven\n", $label));
        exit(1);
    }
}

printf("is_object() branch reached for %d of %d callable shape(s)\n", 2, count($cases));
exit(0);
