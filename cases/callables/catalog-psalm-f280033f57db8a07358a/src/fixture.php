<?php
declare(strict_types=1);
/** @return Closure(int): */
function malformed(): callable { return static function (): void {}; }
/** @return Closure():void */
function control(): Closure { return static function (): void {}; }
