<?php
declare(strict_types=1);
function makeObject(): object { return (object)['a' => 42]; }
/** @param object{hmm: float} $value */
function consume(object $value): float { return $value->hmm; }
function probe(): float { return consume(makeObject()); }
