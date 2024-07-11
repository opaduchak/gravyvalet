import enum
import typing

from .enum_utils import enum_names


__all__ = ("enum_names_same_as", "enum_names_subset")

_ThisEnum = typing.TypeVar("_ThisEnum", bound=type[enum.Enum])


def enum_names_same_as(
    other_enum: type[enum.Enum],
) -> typing.Callable[[_ThisEnum], _ThisEnum]:
    def _enum_decorator(this_enum: _ThisEnum) -> _ThisEnum:
        _other_names = enum_names(other_enum)
        _these_names = enum_names(this_enum)
        if _other_names != _these_names:
            _missing = (_other_names - _these_names) or None
            _extras = (_these_names - _other_names) or None
            raise RuntimeError(
                f"enum_names_same: enum names not same! {this_enum} should follow {other_enum}"
                f"\n\tmissing: {_missing}"
                f"\n\textras: {_extras}"
            )
        return this_enum

    return _enum_decorator


def enum_names_subset(
    other_enum: type[enum.Enum],
) -> typing.Callable[[_ThisEnum], _ThisEnum]:
    def _enum_decorator(this_enum: _ThisEnum) -> _ThisEnum:
        _other_names = enum_names(other_enum)
        _these_names = enum_names(this_enum)
        if not _these_names.issubset(_other_names):
            _extras = (_these_names - _other_names) or None
            raise RuntimeError(
                f"enum_names_same: {this_enum} enum names are not subset of {other_enum}"
                f"\n\textras: {_extras}"
            )
        return this_enum

    return _enum_decorator
