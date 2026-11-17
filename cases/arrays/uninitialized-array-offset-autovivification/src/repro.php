<?php

declare(strict_types=1);

namespace Bench\Arrays\UninitializedArrayOffsetAutovivification;

/**
 * @return array{offset: int, limit: int}
 */
function buildPagination(int $offset, int $limit): array
{
    $result['offset'] = $offset;
    $result['limit'] = $limit;
    $result['limit'] = min($result['limit'], 100);

    return $result;
}
