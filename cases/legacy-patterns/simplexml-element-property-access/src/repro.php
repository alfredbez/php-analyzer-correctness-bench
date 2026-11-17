<?php

declare(strict_types=1);

namespace Bench\LegacyPatterns\SimpleXmlElementPropertyAccess;

function readBookTitle(\SimpleXMLElement $xml): ?string
{
    if (!isset($xml->title)) {
        return null;
    }

    return (string) $xml->title;
}
