<?php
declare(strict_types=1);

function attribute(DOMElement $element): ?string {
    $attribute = $element->attributes->getNamedItem('class');
    if ($attribute === null) { return null; }
    return $attribute->value;
}
