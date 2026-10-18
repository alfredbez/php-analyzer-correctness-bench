<?php
declare(strict_types=1);
#[AllowDynamicProperties]
class Bag {}
function probe(): Bag {
    $bag = new Bag();
    $bag->label = 'stored';
    return $bag;
}
