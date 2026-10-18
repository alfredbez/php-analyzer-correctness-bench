<?php
declare(strict_types=1);
function seconds(string $part, bool $micro): string {
    switch (true) {
        case $part === 'min' && $micro: $result = '00.0'; break;
        case $part === 'min' && !$micro: $result = '00'; break;
        case $part === 'max': $result = '59'; break;
    }
    return $result;
}
/** @param callable(): string $work */
function finish(callable $work): void {
    try { $result = $work(); }
    catch (Exception $error) { $result = 'caught'; }
    finally { echo $result; }
}
