<?php
declare(strict_types=1);
/** @param array{arr: list<string>, a: string, c: int} $args */
function probe(array $args): string {
    extract($args);
    $out = '';
    if ((empty($arr) && empty($a)) || $c === 0) {
        return 'skip';
    } else {
        foreach ($arr as $part) { $out .= strtoupper($part); }
    }
    return $out;
}
