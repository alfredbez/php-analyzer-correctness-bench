<?php
declare(strict_types=1);

trait Maker {
    public function made(): int {
        $object = new class { public function value(): int { return 7; } };
        return $object->value();
    }
}
final class Host { use Maker; }
