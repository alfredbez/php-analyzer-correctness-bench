<?php

declare(strict_types=1);

// Runtime side of the ground truth. Box declares @template T with
// @return T on get(), so a parameter annotated Box<Cat> tells the caller that
// get() hands back a Cat. The runtime decides the two halves of that statement
// independently: a Cat really has meow() and really has no bark(), and value
// dispatch names Cat when the call goes to a method Cat does not declare.

require __DIR__ . '/../src/repro.php';

use function Bench\Generics\ClassTemplateSubstitutionMemberType\bark_of_cat;
use function Bench\Generics\ClassTemplateSubstitutionMemberType\bark_of_dog;
use function Bench\Generics\ClassTemplateSubstitutionMemberType\meow_of_cat;

use Bench\Generics\ClassTemplateSubstitutionMemberType\Box;
use Bench\Generics\ClassTemplateSubstitutionMemberType\Cat;
use Bench\Generics\ClassTemplateSubstitutionMemberType\Dog;

// The two member sets are disjoint, so a member access can only be judged
// against the class the type argument names.
if (!method_exists(Dog::class, 'bark') || method_exists(Cat::class, 'bark')) {
    fwrite(STDERR, "the fixture no longer separates Dog::bark() from Cat\n");
    exit(1);
}

if (!method_exists(Cat::class, 'meow') || method_exists(Dog::class, 'meow')) {
    fwrite(STDERR, "the fixture no longer separates Cat::meow() from Dog\n");
    exit(1);
}

// The substituted type is real at runtime: the value inside a Box<Cat> is a Cat,
// which is why meow() resolves and bark() does not.
if (bark_of_dog(new Box(new Dog())) !== 'woof') {
    fwrite(STDERR, "bark_of_dog() did not dispatch to Dog::bark()\n");
    exit(1);
}

if (meow_of_cat(new Box(new Cat())) !== 'meow') {
    fwrite(STDERR, "meow_of_cat() did not dispatch to Cat::meow()\n");
    exit(1);
}

// The call under test: the same member access on the same generic class, only
// the type argument differs, and the runtime names the substituted class.
$error = null;
try {
    bark_of_cat(new Box(new Cat()));
} catch (Error $thrown) {
    $error = $thrown;
}

if ($error === null) {
    fwrite(STDERR, "bark_of_cat() resolved a Cat::bark(); the annotation is not load-bearing\n");
    exit(1);
}

if (strpos($error->getMessage(), 'Cat::bark') === false) {
    fwrite(STDERR, sprintf("unexpected failure: %s\n", $error->getMessage()));
    exit(1);
}

printf(
    "Box<Cat>::get() returns a Cat, which has no bark(): %s\n",
    $error->getMessage()
);
exit(0);
