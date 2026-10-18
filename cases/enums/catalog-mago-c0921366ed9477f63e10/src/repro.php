<?php
declare(strict_types=1);
enum Locale: string {
    case German='de-DE'; case French='fr-FR';
    public function language(): string { return substr($this->value,0,2); }
}
final class Resolver {
    private const MAP=['DE'=>Locale::German,'FR'=>Locale::French];
    public function resolve(string $key): ?string {
        if (!isset(self::MAP[$key])) { return null; }
        return self::MAP[$key]->language();
    }
}
