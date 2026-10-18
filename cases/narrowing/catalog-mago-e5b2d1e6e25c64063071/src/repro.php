<?php
declare(strict_types=1);
/** @param 'a'|'b' $value */
function probe(string $value): string {
    switch ($value) {
        case 'a': $text='first'; break;
        case 'b': $text='second'; break;
    }
    return $text;
}
