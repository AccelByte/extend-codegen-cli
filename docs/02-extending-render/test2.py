# test2.py

from random import randint
from typing import Any


class Test2Processor:
    def __call__(self, raw: Any, /, **kwargs) -> Any:
        return f"{str(raw)} " * randint(1, 3)
