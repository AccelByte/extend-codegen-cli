# test3/__init__.py

from typing import Any

from jinja2 import Environment
from jinja2.ext import Extension


class MyExtension(Extension):
    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        environment.filters["my"] = self.my_filter

    def my_filter(self, value: Any) -> Any:
        return f"my {str(value)}"
