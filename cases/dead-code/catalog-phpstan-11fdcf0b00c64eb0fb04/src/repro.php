<?php
declare(strict_types=1);

final class DynamicRead {
    public string $value;
    public function __construct(string $secret) {
        $name = 'secret';
        $this->value = $$name;
    }
}
