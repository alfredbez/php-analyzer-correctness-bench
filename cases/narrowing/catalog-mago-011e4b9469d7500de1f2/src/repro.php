<?php
declare(strict_types=1);
function probe(int $tag, bool $stop): bool {
    switch ($tag) {
        case 0:
            if ($stop) { break; }
        default:
            $ready = true;
    }
    return $ready;
}
