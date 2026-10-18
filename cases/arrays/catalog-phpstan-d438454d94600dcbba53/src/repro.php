<?php
declare(strict_types=1);

/** @return int<1, 4> */
function appendCount(int $a, int $b, int $c): int {
    $values = ['base'];
    if ($a > 0) { $values[] = 'x'; } elseif ($a < 0) { $values[] = 'y'; }
    if ($b > 0) { $values[] = 'z'; }
    if ($c === 1) { $values[] = 'p'; } elseif ($c === 2) { $values[] = 'q'; }
    return count($values);
}
