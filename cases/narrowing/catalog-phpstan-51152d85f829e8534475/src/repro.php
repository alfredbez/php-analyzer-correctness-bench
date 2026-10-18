<?php
declare(strict_types=1);

function mayFail(bool $fail): void { if ($fail) { throw new RuntimeException(); } }
function caught(bool $condition, bool $fail): bool {
    try {
        mayFail($fail);
        if ($condition) { throw new InvalidArgumentException(); }
    } catch (Exception $error) { return $condition; }
    return false;
}
