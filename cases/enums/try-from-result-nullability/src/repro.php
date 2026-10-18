<?php

declare(strict_types=1);

namespace Bench\Enums\TryFromResultNullability;

enum Status: string
{
    case Active = 'active';
    case Retired = 'retired';
}

function label(Status $status): string
{
    return $status->value;
}

function label_of_known(): string
{
    return label(Status::tryFrom('active'));
}

function label_of_unknown(string $raw): string
{
    return label(Status::tryFrom($raw));
}
