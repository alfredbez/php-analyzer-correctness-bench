<?php
declare(strict_types=1);
require __DIR__ . '/../src/repro.php';
function check(bool $ok): void { if (!$ok) { throw new RuntimeException('runtime control failed'); } }
$pdo = new PDO('sqlite::memory:');
$query = $pdo->query('SELECT 7 AS value'); check($query instanceof PDOStatement);
$row = nextRow($query); check($row instanceof Row && $row->value === 7);
check(nextRow($query) === null);
