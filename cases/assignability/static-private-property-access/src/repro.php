<?php

declare(strict_types=1);

namespace Bench\Assignability\StaticPrivatePropertyAccess;

class BaseCounter
{
    private static int $count = 1;

    public static function readCount(): int
    {
        return static::$count;
    }
}

final class SubCounter extends BaseCounter
{
    private static int $count = 2;

    public static function readSubCount(): int
    {
        return self::$count;
    }
}
