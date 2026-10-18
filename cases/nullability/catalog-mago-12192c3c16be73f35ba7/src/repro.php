<?php
declare(strict_types=1);
final class Holder { public ?string $text = null; }
function probe(?Holder $holder): string {
    if (!empty($holder->text)) {
        return strtoupper($holder->text);
    }
    return 'absent';
}
