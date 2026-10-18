<?php
declare(strict_types=1);
final class FinalItem {}
/** @param class-string $class */
function construct(string $class): FinalItem {
    if (!is_subclass_of($class, FinalItem::class)) { throw new LogicException('no subclass of a final class'); }
    /** @var FinalItem $instance */
    $instance = new $class();
    return $instance;
}
