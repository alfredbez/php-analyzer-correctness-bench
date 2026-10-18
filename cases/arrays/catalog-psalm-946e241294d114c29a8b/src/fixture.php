<?php
declare(strict_types=1);
/** @return list<int> */
function replace(): array {
    $values = ['north', 'south'];
    sort($values);
    $values = [0, 1];
    return $values;
}
