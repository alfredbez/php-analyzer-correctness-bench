<?php

declare(strict_types=1);

namespace Bench\DeadCode\CatchNeverThrownInUnion;

final class MissingItemException extends \Exception
{
}

final class StaleStateException extends \Exception
{
}

/**
 * @throws MissingItemException
 */
function loadCount(bool $fail): int
{
    if ($fail) {
        throw new MissingItemException('missing');
    }

    return 3;
}

function safeLoadCount(bool $fail): int
{
    try {
        return loadCount($fail);
    } catch (MissingItemException | StaleStateException) {
        return 0;
    }
}
