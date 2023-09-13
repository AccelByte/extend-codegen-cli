# test4.py

from datetime import datetime
from typing import Any

from jinja2 import Environment


class MyRenderer:
    # noinspection PyShadowingBuiltins
    def __call__(
        self, input: Any, template: Any, environment: Environment, /, **kwargs
    ) -> str:
        assert isinstance(input, dict), "input is not if dict type"
        assert isinstance(template, str), "template is not if str type"

        input.setdefault("day", datetime.now().strftime("%A"))

        j2_template = environment.from_string(template)
        out = j2_template.render(input)

        return out
