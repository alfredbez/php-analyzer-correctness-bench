<?php

declare(strict_types=1);

// Runtime side of the ground truth. A match expression without a default arm
// must handle every possible subject value; an unhandled one throws
// UnhandledMatchError. Suit has two cases and label() handles one of them.

require __DIR__ . '/../src/repro.php';

use Bench\Enums\MatchNotExhaustive\Suit;
use function Bench\Enums\MatchNotExhaustive\label;
use function Bench\Enums\MatchNotExhaustive\label_all;

if (Suit::cases() !== [Suit::Hearts, Suit::Spades]) {
    fwrite(STDERR, "Suit does not have exactly the two expected cases\n");
    exit(1);
}

// Asymmetric control: the exhaustive sibling returns for the case the
// non-exhaustive one leaks, and for the covered one.
if (label_all(Suit::Spades) !== 'spades' || label_all(Suit::Hearts) !== 'hearts') {
    fwrite(STDERR, "label_all() did not handle both cases\n");
    exit(1);
}

if (label(Suit::Hearts) !== 'hearts') {
    fwrite(STDERR, "label(Suit::Hearts) is not 'hearts'\n");
    exit(1);
}

try {
    label(Suit::Spades);
} catch (UnhandledMatchError $error) {
    printf("label(Suit::Spades) threw %s; label_all() handled it\n", UnhandledMatchError::class);
    exit(0);
}

fwrite(STDERR, "label(Suit::Spades) returned instead of throwing; Suit::Spades is handled\n");
exit(1);
