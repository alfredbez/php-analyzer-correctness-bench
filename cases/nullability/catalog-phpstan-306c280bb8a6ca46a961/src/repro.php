<?php
declare(strict_types=1);

/**
 * @param array<string, string|null> $files
 * @return array<string, string>
 */
function fill(array $files): array {
    foreach ($files as $path => $content) {
        if ($files[$path] === null) { $files[$path] = 'content'; }
        $files[$path] = strtoupper($files[$path]);
    }
    return $files;
}
