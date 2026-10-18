<?php
declare(strict_types=1);

function anonymousValue(): int {
    $value = new class {
        public int $number = 7;
        public function read(): int { return $this->number; }
    };
    return $value->read() + $value->number;
}
