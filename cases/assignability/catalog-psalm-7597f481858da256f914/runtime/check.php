<?php
function runPhp(array $arguments): array {
    $process = proc_open(array_merge([PHP_BINARY], $arguments), [1 => ['pipe', 'w'], 2 => ['pipe', 'w']], $pipes);
    if (!is_resource($process)) { exit(1); }
    $output = stream_get_contents($pipes[1]) . stream_get_contents($pipes[2]);
    fclose($pipes[1]);
    fclose($pipes[2]);
    return [proc_close($process), $output];
}
[$code, $output] = runPhp([__DIR__ . '/../src/probe.php']);
if ($code === 0 || !str_contains($output, 'must be protected(set)')) { fwrite(STDERR, $output); exit(2); }
[$code] = runPhp(['-r', 'class A { public protected(set) int $value = 1; } final class B extends A { public protected(set) int $value = 2; }']);
if ($code !== 0) { exit(3); }
