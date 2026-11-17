<?php

declare(strict_types=1);

namespace Bench\DeadCode\GetObjectVarsReadsPrivateProperties;

final class MessageDto implements \JsonSerializable
{
    public function __construct(
        private string $type,
        private ?string $body = null,
    ) {}

    /**
     * @return mixed[]
     */
    #[\Override]
    public function jsonSerialize(): array
    {
        return get_object_vars($this);
    }
}

function encodeMessage(MessageDto $dto): string
{
    return json_encode($dto, JSON_THROW_ON_ERROR);
}
