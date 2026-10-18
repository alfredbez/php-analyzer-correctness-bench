<?php

declare(strict_types=1);

namespace Bench\Arrays\NumericStringArrayKey;

function accept_string(string $_): void {}

/** @param array{10?: string} $data */
function fetch(array $data): void
{
    if (array_key_exists('10', $data)) {
        accept_string($data[10]);
    }

    if (isset($data['10'])) {
        accept_string($data['10']);
    }
}
