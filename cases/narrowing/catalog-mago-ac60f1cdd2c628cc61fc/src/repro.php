<?php
declare(strict_types=1);
final class Left { public function left(): string { return 'left'; } }
final class Right { public function right(): string { return 'right'; } }
function probe(Left|Right $value): string {
    switch (get_class($value)) {
        case Left::class: return $value->right();
    }
    return 'other';
}
