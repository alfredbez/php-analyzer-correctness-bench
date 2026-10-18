<?php
declare(strict_types=1);

final class Row { public int $value = 0; }
function nextRow(PDOStatement $statement): ?Row {
    $row = $statement->fetchObject(Row::class);
    return $row === false ? null : $row;
}
