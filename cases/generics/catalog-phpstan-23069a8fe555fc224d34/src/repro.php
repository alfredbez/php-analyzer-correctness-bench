<?php
declare(strict_types=1);

/** @template T */
trait ValueTrait {
    /** @return T */
    abstract public function value();
}
final class IntValue {
    /** @use ValueTrait<int> */
    use ValueTrait;
    #[Override]
    public function value() { return 7; }
}
function consume(IntValue $value): int { return $value->value(); }
