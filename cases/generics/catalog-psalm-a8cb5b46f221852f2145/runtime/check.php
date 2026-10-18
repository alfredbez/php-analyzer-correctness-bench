<?php
require __DIR__ . '/../src/fixture.php';
if (!(new IncompleteBound() instanceof IncompleteBound)) { throw new RuntimeException('comments do not affect PHP'); }
