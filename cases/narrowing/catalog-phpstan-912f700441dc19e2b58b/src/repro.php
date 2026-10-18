<?php
declare(strict_types=1);

function caughtMessage(?string $value): string {
    if ($value !== null) { return $value; }
    try { throw new RuntimeException('caught'); }
    catch (RuntimeException $value) { return $value->getMessage(); }
}
