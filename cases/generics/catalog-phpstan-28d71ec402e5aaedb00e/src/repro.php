<?php
declare(strict_types=1);

/**
 * @template TKey of string
 * @param TKey $key
 * @return array{TKey: int}
 */
function keyed(string $key): array { return [$key => 7]; }
function readSlot(): int { return keyed('slot')['slot']; }
