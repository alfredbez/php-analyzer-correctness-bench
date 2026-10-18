<?php
declare(strict_types=1);
/**
 * @return list<
 *     array{
 *         href: string,
 *         lang: string
 *     }
 * >
 */
function links(): array { return [['href' => '/en', 'lang' => 'en']]; }
function language(): string { return links()[0]['lang']; }
