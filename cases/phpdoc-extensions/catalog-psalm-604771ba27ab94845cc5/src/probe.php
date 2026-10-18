<?php
declare(strict_types=1);
class Holder {
    /** @var null|(\DateTime&\DateTimeImmutable) */
    public $value = null;
}
function probe(): Holder { return new Holder(); }
