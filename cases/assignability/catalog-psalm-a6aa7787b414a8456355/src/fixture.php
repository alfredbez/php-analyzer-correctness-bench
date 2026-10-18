<?php
declare(strict_types=1);
class LocalFailure extends Exception {
    /** @throws self */
    public static function fail(): void { throw new self('local'); }
}
