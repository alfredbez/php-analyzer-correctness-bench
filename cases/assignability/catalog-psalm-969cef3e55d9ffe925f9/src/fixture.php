<?php
declare(strict_types=1);
function joinFields(string $name, string $required, string $id = ''): string { return $name . $required . $id; }
function bad(): string { return joinFields(name: 'N', id: 'I'); }
function good(): string { return joinFields(id: 'I', required: 'R', name: 'N'); }
