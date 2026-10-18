<?php
declare(strict_types=1);

function shifted(DateTimeImmutable $date, string $modifier): string {
    return $date->modify($modifier)->format('Y-m-d');
}
