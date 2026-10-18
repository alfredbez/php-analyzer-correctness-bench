<?php

declare(strict_types=1);

// Runtime side of the ground truth. Bag declares @template-covariant T, so the
// declaration promises that a Bag<Dog> may be used wherever a Bag<Animal> is
// expected - that is what covariance buys the caller. It also declares push()
// with @param T, a write position. Those two promises cannot both hold: put_cat()
// accepts a Bag<Animal> and writes a Cat through that view, the original holder
// of a Bag<Dog> then reads a Cat where its annotation promises a Dog, and the
// native return type of adopt() enforces exactly that promise.

require __DIR__ . '/../src/repro.php';

use function Bench\Generics\CovariantTemplateInWritePosition\adopt;
use function Bench\Generics\CovariantTemplateInWritePosition\put_cat;
use function Bench\Generics\CovariantTemplateInWritePosition\run;

use Bench\Generics\CovariantTemplateInWritePosition\Bag;
use Bench\Generics\CovariantTemplateInWritePosition\Cat;
use Bench\Generics\CovariantTemplateInWritePosition\Dog;

// The sibling classes are unrelated: a Cat is not a Dog, so a Cat written into a
// Bag<Dog> makes the caller's guarantee false independently of any analyzer.
if ((new Cat()) instanceof Dog) {
    fwrite(STDERR, "Cat is a Dog; the fixture no longer witnesses the write\n");
    exit(1);
}

// The honest path: a fresh Bag<Dog> holding a Dog reads back a Dog.
$fresh = new Bag(new Dog());
if (!$fresh->get() instanceof Dog) {
    fwrite(STDERR, "a fresh Bag constructed with a Dog did not read back a Dog\n");
    exit(1);
}

// The write through the widened view: put_cat() is typed Bag<Animal>, which
// covariance makes the Bag<Dog> acceptable to, and it stores a Cat in the very
// box the caller annotated as Bag<Dog>.
$holder = new Bag(new Dog());
put_cat($holder);
if (!$holder->get() instanceof Cat) {
    fwrite(STDERR, "put_cat() did not write a Cat through the widened view\n");
    exit(1);
}

// The consequence: adopt() is annotated Bag<Dog> and declares a native Dog
// return type, so the Cat that covariance let in reaches that return type and
// the call fails. This is the fact the case is about - the covariant
// declaration plus a write position is unsound, not merely unidiomatic.
$type_error = null;
try {
    run();
} catch (TypeError $error) {
    $type_error = $error;
}

if ($type_error === null) {
    fwrite(STDERR, "run() returned; the Cat did not reach adopt()'s Dog return type\n");
    exit(1);
}

if (strpos($type_error->getMessage(), 'adopt') === false
    || strpos($type_error->getMessage(), 'Dog') === false
    || strpos($type_error->getMessage(), 'Cat') === false) {
    fwrite(STDERR, sprintf("unexpected failure: %s\n", $type_error->getMessage()));
    exit(1);
}

printf(
    "put_cat() stored a Cat in a Bag<Dog> through the covariant widening; adopt() failed on its Dog return type: %s\n",
    $type_error->getMessage()
);
exit(0);
