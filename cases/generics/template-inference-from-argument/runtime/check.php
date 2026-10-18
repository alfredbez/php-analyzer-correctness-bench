<?php

declare(strict_types=1);

// Runtime side of the ground truth. identity() is documented as
// @template T / @param T / @return T, so the call identity(5) has the value 5
// and type int. Under declare(strict_types=1) an int is not accepted for a
// string parameter, so strlen(identity(5)) throws; strlen(identity('abc')) is
// the asymmetric control that runs.

require __DIR__ . '/../src/repro.php';

use function Bench\Generics\TemplateInferenceFromArgument\identity;
use function Bench\Generics\TemplateInferenceFromArgument\length_of_int;
use function Bench\Generics\TemplateInferenceFromArgument\length_of_string;

// The @return T promise holds at runtime: the value comes back unchanged, so
// the argument type is the result type.
if (identity(5) !== 5) {
    fwrite(STDERR, "identity(5) did not return 5\n");
    exit(1);
}

if (length_of_string() !== 3) {
    fwrite(STDERR, sprintf("length_of_string() returned %s\n", var_export(length_of_string(), true)));
    exit(1);
}

try {
    length_of_int();
} catch (TypeError $error) {
    if (strpos($error->getMessage(), 'strlen') === false) {
        fwrite(STDERR, sprintf("unexpected TypeError: %s\n", $error->getMessage()));
        exit(1);
    }

    printf("strlen(identity('abc')) = 3; strlen(identity(5)) throws: %s\n", $error->getMessage());
    exit(0);
}

fwrite(STDERR, "strlen(identity(5)) did not throw; the int did not reach strlen under strict_types\n");
exit(1);
