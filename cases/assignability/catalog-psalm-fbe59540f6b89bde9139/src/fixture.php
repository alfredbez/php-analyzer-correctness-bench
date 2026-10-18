<?php
declare(strict_types=1);
/** @param ('red"quoted'|'blue'|1|2|3) $value */
function accept(string|int $value): string|int { return $value; }
function valid(): bool {
    return accept('red"quoted') === 'red"quoted' && accept('blue') === 'blue' && accept(1) === 1 && accept(2) === 2 && accept(3) === 3;
}
