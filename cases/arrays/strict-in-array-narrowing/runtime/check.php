<?php

declare(strict_types=1);

// Runtime side of the ground truth. With the third argument true, in_array()
// compares with ===, so a value is in the haystack only if it is identical to
// an element. The fixture's needle is declared string|bool and its haystack
// elements are 'a', 'b' or an int; over exactly those needle types a true result
// means the needle is 'a' or 'b', because no bool and no string is identical to
// an int.

require __DIR__ . '/../src/repro.php';

use function Bench\Arrays\StrictInArrayNarrowing\narrow;

$haystacks = [
    ['a', 'b', 1],
    ['a', 'b'],
    [1, 0],
    [],
    ['b', 2, 'a'],
];

// The needle sample mirrors the declared type of the fixture's parameter.
$needles = [true, false, 'a', 'b', '1', '0', '', 'a1', 'b0'];

$matches = 0;
foreach ($haystacks as $haystack) {
    foreach ($needles as $needle) {
        if (!in_array($needle, $haystack, true)) {
            continue;
        }

        $matches++;
        if ($needle !== 'a' && $needle !== 'b') {
            fwrite(STDERR, sprintf(
                "strict in_array matched %s in %s; the narrowing claim is false\n",
                var_export($needle, true),
                var_export($haystack, true)
            ));
            exit(1);
        }
    }
}

if ($matches === 0) {
    fwrite(STDERR, "the sample produced no match at all; the claim is not exercised\n");
    exit(1);
}

// The third argument is what carries the claim, not the values alone. An int
// needle does match an int element under ===, and the same '1'/1 pair matches
// only in the loose form.
if (!in_array(1, [1], true)) {
    fwrite(STDERR, "strict in_array(1, [1]) is false\n");
    exit(1);
}

if (in_array('1', [1], true)) {
    fwrite(STDERR, "strict in_array('1', [1]) is true; strings and ints are not compared with ===\n");
    exit(1);
}

if (!in_array('1', [1], false)) {
    fwrite(STDERR, "loose in_array('1', [1]) is false; the loose control is wrong\n");
    exit(1);
}

// The fixture's guard is exercised for a match and for a miss.
narrow('a', ['a', 'b', 1]);
narrow(false, ['a', 'b', 1]);

printf("%d strict match(es) over %d needle/haystack pair(s), all 'a'/'b'\n", $matches, count($haystacks) * count($needles));
exit(0);
