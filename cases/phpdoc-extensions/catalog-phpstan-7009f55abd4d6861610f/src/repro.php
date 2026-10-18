<?php
declare(strict_types=1);

/** @method string text() */
final class MagicText {
    /** @param list<mixed> $arguments */
    public function __call(string $name, array $arguments): string { return $name; }
}
function magicText(MagicText $object): string { return $object->text(); }
