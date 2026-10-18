<?php
declare(strict_types=1);

function shifted(DateTimeImmutable $date, string $modifier): ?string {
    $result = $date->modify($modifier);
    return $result === false ? null : $result->format('Y-m-d');
}
