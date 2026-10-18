<?php
declare(strict_types=1);

/**
 * @param array{foo: int, 2: string} $input
 * @return array{FOO: int, 2: string}
 */
function upperKeys(array $input): array { return array_change_key_case($input, CASE_UPPER); }
