<?php
declare(strict_types=1);

final class IncludedRead {
    public string $value;
    public function __construct(string $input) { require __DIR__ . '/../support/read.inc.php'; }
}
