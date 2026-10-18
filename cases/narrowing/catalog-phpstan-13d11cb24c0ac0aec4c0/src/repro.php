<?php
declare(strict_types=1);

function remaining(Throwable $value): ?Error {
    if ($value instanceof Exception) { return null; }
    return $value;
}
