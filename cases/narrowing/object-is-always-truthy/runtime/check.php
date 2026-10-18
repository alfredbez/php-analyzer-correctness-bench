<?php

declare(strict_types=1);

// Token is user-defined and has no custom boolean cast. Internal objects with
// custom casts are excluded; the claim is not universal across all objects.
// The samples below cover the shapes a legacy codebase produces (plain object,
// object with a null property, object with __toString, closure).

require __DIR__ . '/../src/repro.php';

use Bench\Narrowing\ObjectIsAlwaysTruthy\Token;

use function Bench\Narrowing\ObjectIsAlwaysTruthy\is_falsy;

class Emptyish
{
    public ?string $name = null;
}

class StringableValue
{
    public function __toString(): string
    {
        return '';
    }
}

$samples = [
    new Token(),
    new \stdClass(),
    new Emptyish(),
    new StringableValue(),
    static function (): void {},
];

foreach ($samples as $sample) {
    if ((bool) $sample !== true) {
        fwrite(STDERR, sprintf("%s is not truthy\n", get_class($sample)));
        exit(1);
    }
}

if (is_falsy(new Token()) !== false) {
    fwrite(STDERR, "the dead branch was entered\n");
    exit(1);
}

printf("%d object shape(s) cast to true; is_falsy() stayed on the live path\n", count($samples));
exit(0);
