<?php

declare(strict_types=1);

// Runtime side of the ground truth. An iterable parameter is "array or
// Traversable", while count() is documented to accept "array or Countable". A
// Generator is a Traversable that is not Countable, so the fixture cannot assume
// that its parameter is countable: the call throws a TypeError.

require __DIR__ . '/../src/repro.php';

use function Bench\LegacyPatterns\CountOnIterable\row_count;

if (row_count(['a', 'b', 'c']) !== 3) {
    throw new RuntimeException('The array control was not counted correctly');
}

if (row_count(new ArrayIterator(['a', 'b'])) !== 2) {
    throw new RuntimeException('A Countable Traversable must remain supported');
}

$generator = (static function (): Generator {
    yield 'a';
    yield 'b';
})();

try {
    row_count($generator);
} catch (TypeError $error) {
    printf("count() rejected a Generator: %s\n", $error->getMessage());
    exit(0);
}

fwrite(STDERR, "count() counted a Generator, but a Generator is not Countable\n");
exit(1);
