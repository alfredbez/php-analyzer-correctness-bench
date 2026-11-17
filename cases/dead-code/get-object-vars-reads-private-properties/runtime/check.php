<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use Bench\DeadCode\GetObjectVarsReadsPrivateProperties\MessageDto;
use function Bench\DeadCode\GetObjectVarsReadsPrivateProperties\encodeMessage;

$dto = new MessageDto('system', 'ready');
$vars = $dto->jsonSerialize();
if ($vars !== ['type' => 'system', 'body' => 'ready']) {
    fwrite(STDERR, sprintf("Unexpected jsonSerialize() result: %s\n", var_export($vars, true)));
    exit(1);
}

$encoded = encodeMessage($dto);
if ($encoded !== '{"type":"system","body":"ready"}') {
    fwrite(STDERR, sprintf("Unexpected JSON: %s\n", $encoded));
    exit(1);
}

echo "get_object_vars(\$this) reads private properties at runtime\n";
exit(0);
