<?php

declare(strict_types=1);

namespace Bench\Assignability\DocblockParameterContravariance;

class Constraint {}

final class LengthConstraint extends Constraint
{
    public function minLength(): int
    {
        return 3;
    }
}

abstract class BaseValidator
{
    public function validate(mixed $value, Constraint $constraint): bool
    {
        return $value !== null;
    }
}

final class LengthValidator extends BaseValidator
{
    /**
     * @param string $value
     * @param LengthConstraint $constraint
     */
    #[\Override]
    public function validate(mixed $value, Constraint $constraint): bool
    {
        return strlen($value) >= $constraint->minLength();
    }
}

function check(BaseValidator $validator, mixed $value, Constraint $constraint): bool
{
    return $validator->validate($value, $constraint);
}
