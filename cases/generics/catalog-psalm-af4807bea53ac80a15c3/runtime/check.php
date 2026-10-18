<?php
require __DIR__ . '/../src/fixture.php';
if (language() !== 'en' || links() !== [['href' => '/en', 'lang' => 'en']]) { throw new RuntimeException('multiline list shape'); }
