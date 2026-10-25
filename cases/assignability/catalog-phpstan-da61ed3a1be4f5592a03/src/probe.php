<?php
declare(strict_types=1);

final class FixedReading {
    public readonly int $value;

    public function __construct(int $value) {
        $this->value = $value;
    }

    public function replace(int $value): void {
        $this->value = $value;
    }
}
