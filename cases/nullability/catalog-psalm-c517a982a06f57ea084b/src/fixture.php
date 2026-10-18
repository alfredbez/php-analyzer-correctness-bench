<?php
declare(strict_types=1);
/** @return stdClass */
function maybe(bool $present): ?stdClass { return $present ? new stdClass() : null; }
function guarded(bool $present): bool {
    $value = maybe($present);
    return $value !== null;
}
