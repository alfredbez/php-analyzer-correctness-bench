<?php
class ParentValue {
    public protected(set) int $value = 1;
}
final class ChildValue extends ParentValue {
    public private(set) int $value = 2;
}
