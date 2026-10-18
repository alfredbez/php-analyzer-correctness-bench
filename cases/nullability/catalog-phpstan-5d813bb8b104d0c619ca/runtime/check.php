<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
$doc = new DOMDocument(); $element = $doc->createElement('item');
check(attribute($element) === null);
$element->setAttribute('class', ''); check(attribute($element) === '');
$element->setAttribute('class', 'kept'); check(attribute($element) === 'kept');
