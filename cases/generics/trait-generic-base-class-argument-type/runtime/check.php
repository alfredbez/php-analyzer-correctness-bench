<?php

declare(strict_types=1);

require __DIR__ . '/../src/repro.php';

use Bench\Generics\TraitGenericBaseClassArgumentType\CustomerEntity;
use Bench\Generics\TraitGenericBaseClassArgumentType\OrderEntity;
use Bench\Generics\TraitGenericBaseClassArgumentType\OrderRepository;

$repository = new OrderRepository(
    static fn (OrderEntity $order): string => $order->orderCode()
);

if ($repository->archive(new OrderEntity()) !== 'ORD-1') {
    fwrite(STDERR, "Expected OrderEntity to archive to 'ORD-1'\n");
    exit(1);
}

try {
    $repository->archive(new CustomerEntity());
    fwrite(STDERR, "Expected TypeError when passing CustomerEntity to OrderRepository::archive()\n");
    exit(1);
} catch (\TypeError $error) {
    if (strpos($error->getMessage(), 'OrderEntity') === false) {
        fwrite(STDERR, sprintf("Unexpected TypeError: %s\n", $error->getMessage()));
        exit(1);
    }
}

echo "Passing CustomerEntity via ArchivableTrait::archive() throws TypeError in OrderRepository\n";
exit(0);
