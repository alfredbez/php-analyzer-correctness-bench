<?php
declare(strict_types=1);

enum Choice { case First; case Second; case Third; }
/** @return Choice::First|null */
function firstOnly(Choice $choice): ?Choice {
    if ($choice === Choice::Second) { return null; }
    if ($choice === Choice::Third) { return null; }
    return $choice;
}
