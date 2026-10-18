<?php
declare(strict_types=1);
/** @param 'a'|'b' $value */
function probe(string $value): string {
    switch ($value) {
        case 'a': return 'first';
        case 'b': return 'second';
        default: throw new LogicException('outside contract');
    }
}
