<?php
declare(strict_types=1);
/** @psalm-type Choice = Left|Right|null */

// The alias still belongs to the following declaration.

class Left {
    /** @return Choice */
    public static function probe(int $branch): Left|Right|null {
        return match ($branch) { 0 => new Left(), 1 => new Right(), default => null };
    }
}
class Right {}
