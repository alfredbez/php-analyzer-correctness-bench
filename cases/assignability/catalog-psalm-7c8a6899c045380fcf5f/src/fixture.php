<?php
declare(strict_types=1);
/** @param 'red'|'blue'|1|2|3 $value */
function accept(string|int $value): string|int { return $value; }
function bad(): string|int { return accept(4); }
function good(): string|int { return accept(3); }
