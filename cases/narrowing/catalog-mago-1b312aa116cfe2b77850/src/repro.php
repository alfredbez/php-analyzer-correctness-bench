<?php
declare(strict_types=1);
function make(): stdClass { return new stdClass(); }
function probe(): string {
    if ($object = make()) { return get_class($object); }
    return 'absent';
}
function control(?stdClass $input): string {
    if ($object = $input) { return get_class($object); }
    return 'absent';
}
