<?php
require __DIR__ . '/../src/probe.php';
set_error_handler(static function (int $level, string $message): never { throw new ErrorException($message, 0, $level); });
if (probe()->label !== 'stored') { exit(1); }
class Plain {}
try { $plain = new Plain(); $plain->label = 'deprecated'; exit(2); } catch (ErrorException $e) {
    if (!str_contains($e->getMessage(), 'dynamic property')) { exit(3); }
}
