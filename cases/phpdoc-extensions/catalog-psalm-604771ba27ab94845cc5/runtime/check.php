<?php
require __DIR__ . '/../src/probe.php';
if (probe()->value !== null || is_a(DateTime::class, DateTimeImmutable::class, true) || is_a(DateTimeImmutable::class, DateTime::class, true)) { exit(1); }
