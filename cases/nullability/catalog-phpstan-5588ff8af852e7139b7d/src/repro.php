<?php
declare(strict_types=1);

final class ChildValue { public static function text(): string { return 'child'; } }
final class ParentValue { public function __construct(public ChildValue $child) {} }
function optionalText(?ParentValue $parent): ?string { return $parent?->child::text(); }
