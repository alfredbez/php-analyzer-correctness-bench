<?php

declare(strict_types=1);

// Runtime side of the ground truth. A string function name is a callable but
// not a Closure: the callable pseudo-type is a union of closures, strings and
// arrays, so a value typed callable is not accepted where \Closure is required.

require __DIR__ . '/../src/repro.php';

use function Bench\Assignability\CallableNotClosure\from_callable;
use function Bench\Assignability\CallableNotClosure\from_closure;
use function Bench\Assignability\CallableNotClosure\from_string_literal;
use function Bench\Assignability\CallableNotClosure\keep;

// The string is callable - the fixture is not about "not callable" - but it is
// not an instance of Closure.
if (!is_callable('phpversion')) {
    fwrite(STDERR, "'phpversion' is not callable; the control is wrong\n");
    exit(1);
}

if (call_user_func('phpversion') === '') {
    fwrite(STDERR, "calling 'phpversion' produced no version string\n");
    exit(1);
}

if ('phpversion' instanceof Closure) {
    fwrite(STDERR, "a string function name is an instance of Closure\n");
    exit(1);
}

// A definite violation: the literal reaches the \Closure parameter.
try {
    from_string_literal();
    fwrite(STDERR, "keep('phpversion') did not throw\n");
    exit(1);
} catch (TypeError $error) {
    // expected: the string is not a Closure
}

// A possible violation: a value typed only as callable may be a string.
try {
    from_callable('strlen');
    fwrite(STDERR, "keep(callable) with a string callable did not throw\n");
    exit(1);
} catch (TypeError $error) {
    // expected: the value is a string, which is not a Closure
}

// Asymmetric control: a real closure is accepted and returned.
$closure = from_closure();

if (!$closure instanceof Closure || $closure() !== 'ok') {
    fwrite(STDERR, "a closure was not accepted for the \\Closure parameter\n");
    exit(1);
}

if (keep(static fn (): string => 'ok')() !== 'ok') {
    fwrite(STDERR, "the closure control did not survive the parameter\n");
    exit(1);
}

printf("'phpversion' is callable but not a Closure; the closure control was accepted\n");
exit(0);
