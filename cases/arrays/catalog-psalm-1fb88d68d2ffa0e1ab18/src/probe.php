<?php
declare(strict_types=1);
/** @param array{test: string} $row */
function readRow(array $row): string { return $row['test']; }
function probe(): string { return readRow(['test' => 'value']); }
