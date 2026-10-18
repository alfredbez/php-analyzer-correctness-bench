<?php
declare(strict_types=1);

final class Item { public string $name = 'kept'; }
final class ItemHolder {
    public function __construct(private ?Item $item) {}
    public function first(): ?Item { return $this->item; }
}
function itemName(ItemHolder $holder): ?string {
    if ($holder->first() !== null) { return $holder->first()->name; }
    return null;
}
