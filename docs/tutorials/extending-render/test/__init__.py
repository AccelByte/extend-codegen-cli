# test/__init__.py

from typing import Any


class TestProcessor:
    def __call__(self, raw: Any, /, **kwargs) -> Any:
        return f"- {str(raw)} -"
