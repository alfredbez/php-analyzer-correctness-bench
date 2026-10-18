<?php
require __DIR__ . '/../src/fixture.php';
foreach ([FinalItem::class, stdClass::class, Exception::class] as $class) {
    if (is_subclass_of($class, FinalItem::class)) { throw new RuntimeException('final class subclass'); }
    try { construct($class); } catch (LogicException $e) { continue; }
    throw new RuntimeException('unreachable construction was reached');
}
