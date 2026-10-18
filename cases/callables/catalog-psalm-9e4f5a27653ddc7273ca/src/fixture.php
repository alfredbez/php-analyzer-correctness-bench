<?php
declare(strict_types=1);
/**
 * @param array{a:Closure():(array<string,int>|null),b?:Closure():(array{label:string,flag:bool}|null)} $callbacks
 * @return array<string,int>|null
 */
function invoke(array $callbacks): ?array { return $callbacks['a'](); }
