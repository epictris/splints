from dataclasses import dataclass
from typing import Callable, Type

from splints.types.server import State


@dataclass(kw_only=True)
class Method[A, R]:
    arg_type: Type[A]
    func: Callable[[A, State], R]


def method[A, R](
    arg_type: Type[A], _: Type[R] | None = None
) -> Callable[[Callable[[A, State], R]], Method[A, R]]:
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return Method(arg_type=arg_type, func=wrapper)

    return decorator
