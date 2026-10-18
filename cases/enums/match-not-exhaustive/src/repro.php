<?php

declare(strict_types=1);

namespace Bench\Enums\MatchNotExhaustive;

enum Suit
{
    case Hearts;
    case Spades;
}

function label(Suit $suit): string
{
    return match ($suit) {
        Suit::Hearts => 'hearts',
    };
}

function label_all(Suit $suit): string
{
    return match ($suit) {
        Suit::Hearts => 'hearts',
        Suit::Spades => 'spades',
    };
}
