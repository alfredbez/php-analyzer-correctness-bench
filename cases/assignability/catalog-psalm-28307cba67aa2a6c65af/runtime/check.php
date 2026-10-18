<?php
require __DIR__ . '/../src/probe.php';
if (consume((object)['hmm' => 1.5]) !== 1.5) { exit(1); }
set_error_handler(static function (int $level, string $message): never { throw new ErrorException($message, 0, $level); });
try { probe(); exit(2); } catch (ErrorException $e) {
    if (!str_contains($e->getMessage(), 'hmm')) { exit(3); }
}
