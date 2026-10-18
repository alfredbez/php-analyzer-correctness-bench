<?php
declare(strict_types=1);

/**
 * @param int<-9, 9> $value
 * @return int<0, 9>
 */
function magnitude(int $value): int { return abs($value); }
