<?php
declare(strict_types=1);
function accept(string|null|object $value): string|null|object { return $value; }
function nullValue(): string|null|object { return accept(null); }
