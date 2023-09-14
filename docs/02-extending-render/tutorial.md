# Extending the render command

## With custom `input-processor` and/or `template-processor`

First, we need to create a custom processor, it should follow this Python protocol:

```python
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Processor(Protocol):
    def __call__(self, raw: Any, /, **kwargs) -> Any:
        ...
```

```python
# test/__init__.py

from typing import Any


class TestProcessor:
    def __call__(self, raw: Any, /, **kwargs) -> Any:
        """This Processor wraps the raw value with spaces and dashes.

        :param self: Processor instance.
        :param raw: Raw value.
        :param kwargs: Additional arguments.
        :return: Wrapped raw value.
        """
        return f"- {str(raw)} -"

```

To use it, we set the import path as either our `-i/--input-processor` or `-t/--template-processor`.

---

```shell
./accelbyte-codegen render --help
```

```text
Usage: accelbyte-codegen render [OPTIONS] INPUT TEMPLATE

  Renders the TEMPLATE using the specified INPUT.

  INPUT: Input value to be passed into the templating engine.  [required]
  TEMPLATE: Template value used to create the template object.  [required]

Options:
  -i, --input-processor TEXT      Sets the processor to use for the INPUT
                                  argument.  [default: yamlf]
  -t, --template-processor TEXT   Sets the processor to use for the TEMPLATE
                                  argument.  [default: textf]
  -r, --renderer TEXT             Sets the renderer to use.  [default:
                                  default]
  -e, --extension TEXT            Additional extensions to use in the template
                                  environment.  [casestyle|collections|ctrlflo
                                  w|datetime|filecontents|jsonptr|regex|safeca
                                  st|string|jinja2.ext.do|jinja2.ext.loopcontr
                                  ols]  [default: *default, *jinja]
  -l, --loader TEXT               Additional template search paths to use in
                                  the template environment.
  -o, --output TEXT               Sets the output target.
                                  [stdout|stderr|<filepath>]  [default:
                                  stdout]
  --inspect [0|n|no|1|y|yes|2|v|verbose]
                                  Simulates the command and displays
                                  information about the template environment.
                                  [default: 0]
  --help                          Show this message and exit.
```

---

```shell
tree
```

```text
.
|-- accelbyte-codegen
|-- test
|   `-- __init__.py
```

---

```shell
./accelbyte-codegen render \
    '{"first_name": "John", "last_name": "Doe"}' \
    'Hello {{ first_name }} {{ last_name }}!' \
    -i json \
    -t 'test.TestProcessor'
```

```text
- Hello John Doe! -
```

---

We can also use regular Python files.

```python
# test2.py

from random import randint
from typing import Any


class Test2Processor:
    def __call__(self, raw: Any, /, **kwargs) -> Any:
        return f"{str(raw)} " * randint(1, 3)

```

---

```shell
tree
```

```text
.
|-- accelbyte-codegen
|-- test2.py
```

---

```shell
./accelbyte-codegen render \
    '{"first_name": "John", "last_name": "Doe"}' \
    'Hello {{ first_name }} {{ last_name }}!' \
    -i json \
    -t 'test2.Test2Processor'
```

```text
Hello John Doe! Hello John Doe! Hello John Doe! 
```

---

## With custom [Jinja] [Extensions] (and [Filters])

Similar to how we use custom processors, we could add one (or many) extension(s) by using the `-e/--extension` argument once (or multiple times, i.e. `-e abc -e def.xyz`).

```python 
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

```

---

```shell
tree
```

```text
.
|-- accelbyte-codegen
|-- test3
|   `-- __init__.py
```

---

```python
./accelbyte-codegen render \
    '{"subject": "Dog"}' \
    'Hello {{ subject | my }}!' \
    -i json \
    -t text \
    -e 'test3.MyExtension'
```

```text
Hello my Dog!
```

---

## With custom `-r/--renderer`

First, we need to create a custom renderer, it should follow this Python protocol:

```python
from typing import Any, Protocol, runtime_checkable

from jinja2 import Environment


@runtime_checkable
class Renderer(Protocol):
    # noinspection PyShadowingBuiltins
    def __call__(
        self, input: Any, template: Any, environment: Environment, /, **kwargs
    ) -> str:
        ...
```

```python
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

        input.setdefault("time", datetime.now().isoformat())

        j2_template = environment.from_string(template)
        out = j2_template.render(input)

        return out

```

---

```shell
tree
```

```text
.
|-- accelbyte-codegen
|-- test4.py
```

---

```shell
./accelbyte-codegen render \
    '{"first_name": "John", "last_name": "Doe"}' \
    'Hello {{ first_name }} {{ last_name }}, today is {{ day }}'! \
    -i json \
    -t text \
    -r 'test4.MyRenderer'
```

```text
Hello John Doe, today is Tuesday!
```

---

This concludes this tutorial.

[Jinja]: https://jinja.palletsprojects.com
[Extensions]: https://jinja.palletsprojects.com/en/3.1.x/templates/#extensions
[Filters]: https://jinja.palletsprojects.com/en/3.1.x/templates/#filters
