<?php
declare(strict_types=1);
final class Group {}
/** @param Group[]| $groups */
function broken(array $groups): int { return count($groups); }
/** @param array<int, Group> $groups */
function valid(array $groups): int { return count($groups); }
