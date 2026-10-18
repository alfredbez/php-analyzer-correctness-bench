<?php
require __DIR__ . '/../src/fixture.php';
if (!(guarded(Known::class) instanceof Known) || guarded('not-a-class') !== null) { throw new RuntimeException('class string guard'); }
