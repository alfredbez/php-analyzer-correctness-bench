<?php
declare(strict_types=1);
/**
 * @psalm-type Middleware = array<
 *     class-string<Exception>,
 *     array<int, string>
 * >
 * @psalm-type Route = array{
 *     rule: string,
 *     middleware?: Middleware
 * }
 */
class Routes {
    /** @param Route $route */
    public static function probe(array $route): string { return $route['rule']; }
}
