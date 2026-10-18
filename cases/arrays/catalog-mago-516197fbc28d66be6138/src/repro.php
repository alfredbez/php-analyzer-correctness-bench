<?php
declare(strict_types=1);
/** @param array<int, array<int, string>>|null $rows */
function probe(?array $rows): string {
    if (is_array($rows)) {
        $text = '';
        foreach ($rows as $row) { $text .= implode(',', $row); }
        return $text;
    }
    return 'absent';
}
