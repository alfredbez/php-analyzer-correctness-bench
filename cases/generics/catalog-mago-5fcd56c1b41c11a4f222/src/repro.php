<?php
declare(strict_types=1);
abstract class Entity {}
final class Product extends Entity {}
/** @template T of Entity */
abstract class Mapper {
    /** @param T $entity */
    public function store(Entity $entity): Entity { return $entity; }
}
/** @template T of Entity
 * @extends Mapper<T> */
abstract class Intermediate extends Mapper {}
final class Direct extends Mapper {
    public function save(Product $entity): Entity { return $this->store($entity); }
}
final class Indirect extends Intermediate {
    public function save(Product $entity): Entity { return $this->store($entity); }
}
/** @extends Mapper<Product> */
final class ProductMapper extends Mapper {}
