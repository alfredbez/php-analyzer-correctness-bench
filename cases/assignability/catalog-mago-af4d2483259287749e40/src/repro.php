<?php
declare(strict_types=1);
class Base {}
final class Child extends Base { public function run(): string { return 'child'; } }
final class Other {}
function probe(Base $value): string {
    $oldClass = get_class($value);
    $value = new Other();
    switch ($oldClass) {
        case Child::class: return $value->run();
    }
    return 'other';
}
