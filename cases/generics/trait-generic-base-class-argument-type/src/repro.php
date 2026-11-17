<?php

declare(strict_types=1);

namespace Bench\Generics\TraitGenericBaseClassArgumentType;

interface EntityInterface
{
}

final class OrderEntity implements EntityInterface
{
    public function orderCode(): string
    {
        return 'ORD-1';
    }
}

final class CustomerEntity implements EntityInterface
{
}

/**
 * @template T of EntityInterface
 */
abstract class BaseRepository
{
    /** @var callable(T): string */
    private $formatter;

    /** @param callable(T): string $formatter */
    public function __construct(callable $formatter)
    {
        $this->formatter = $formatter;
    }

    /** @param T $entity */
    protected function persist(EntityInterface $entity): string
    {
        return ($this->formatter)($entity);
    }
}

/**
 * @require-extends BaseRepository
 */
trait ArchivableTrait
{
    public function archive(EntityInterface $entity): string
    {
        return $this->persist($entity);
    }
}

/**
 * @extends BaseRepository<OrderEntity>
 */
final class OrderRepository extends BaseRepository
{
    use ArchivableTrait;
}
