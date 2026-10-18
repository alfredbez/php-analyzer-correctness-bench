<?php
declare(strict_types=1);
final class Keys { public const BAR='bar'; public const ONE=1; }
/** @param array<string, string> $data */
function strings(array $data): bool {
    if (!empty($data['foo'])) { return empty($data[Keys::BAR]); }
    return false;
}
/** @param array<int, string> $data */
function integers(array $data): bool {
    if (!empty($data[0])) { return empty($data[Keys::ONE]); }
    return false;
}
