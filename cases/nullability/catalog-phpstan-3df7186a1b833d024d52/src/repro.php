<?php
declare(strict_types=1);

function knownDate(): DateTimeImmutable {
    return DateTimeImmutable::createFromFormat('Y-m-d', '2020-10-12');
}
