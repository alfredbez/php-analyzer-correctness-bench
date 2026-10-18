<?php
declare(strict_types=1);
function probe(?Exception $error): string {
    if ($error && $error->getMessage() === 'hello') {
        return 'hello-path';
    } elseif (empty($error)) {
        return 'null-path';
    }
    return $error->getMessage();
}
