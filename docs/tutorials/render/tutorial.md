# Using the render command

First, let's check the render command help text.

```shell
./accelbyte-codegen render --help
```

```text
Usage: accelbyte-codegen render [OPTIONS] INPUT TEMPLATE

Options:
  -i, --input-processor TEXT     [default: yamlf]
  -t, --template-processor TEXT  [default: textf]
  -r, --renderer TEXT            [default: default]
  -e, --extension TEXT           [casestyle|collections|ctrlflow|datetime|file
                                 contents|jsonptr|regex|safecast|string|jinja2
                                 .ext.do|jinja2.ext.loopcontrols]  [default:
                                 *default, *jinja]
  -l, --loader TEXT
  -o, --output TEXT              [stdout|stderr|<filepath>]  [default: stdout]
  --help                         Show this message and exit.
```

---

Now, let's try it out.

```shell
./accelbyte-codegen render \
    '{"first_name": "John", "last_name": "Doe"}' \
    'Hello {{ first_name }} {{ last_name }}!' \
    -i json \
    -t text
```

```text
Hello John Doe!
```

In the example above we pass in:
* the string `{"first_name": "John", "last_name": "Doe"}` as the `INPUT`
* the string `Hello {{ first_name }} {{ last_name }}!` as the `TEMPLATE`
* `json` as our `input-processor`, which will treat and process the `INPUT` string as a JSON object
* `text` as our `template-processor`, which will treat the `TEMPLATE` string as a text

---

Now, let's try again with the `to_snake` filter included in the `CaseStyleExtension` (`-e casestyle`).

```shell
./accelbyte-codegen render \
    '{"greeting": "Hello World"}' \
    'Bot: {{ greeting | to_snake }}!' \
    -i json \
    -t text
```

```text
Bot: hello_world!
```

> :bulb: `accelbyte-codegen` uses [Jinja] under the hood and `to_snake` is just one of the included [filters]. See also [extensions].

---

How about we try inputting a `.json` file instead?

```json5
// data/characters.json

{
  "type": "Characters",
  "battle_cry": "Justice League, Advance!",
  "superheroes": [
    "Aquaman",
    "Batman",
    "Green Lantern",
    "Martian Manhunter",
    "Superman",
    "The Flash",
    "Wonder Woman"
  ],
  "villains": [
    "Black Manta",
    "Cheetah",
    "Joker",
    "Lex Luthor",
    "Ma'alefa'ak",
    "Sinestro",
    "Reverse Flash"
  ]
}
```

```shell
./accelbyte-codegen render \
    'data/characters.json' \
    'Help me {{ superheroes[2] | to_pascal }}!' \
    -i jsonf \
    -t text
```

```text
Help me GreenLantern!
```

Here we've switched to using `jsonf` as our *input-processor*. `jsonf` treats the `INPUT` argument here as a path to file that contains valid JSON. It opens the file, reads, and parses (i.e. `json.loads(...)`) its contents; and passes the parsed object (now a Python object) to the renderer.

> :bulb: this assumes that the `accelbyte-codegen` executable is in the same folder as the 'data' folder.

---

Writing templates in the console is getting hard, how about we move to using files as input too?

```text
{# data/template1.j2 -#}

{% for _ in range(3) %}
It's {{ villains[range(villains | count) | random] | to_camel }}, help me {{ superheroes[range(superheroes | count) | random] | to_camel }}!
{% endfor %}
```

```shell
./accelbyte-codegen render \
    'data/characters.json' \
    'data/template1.j2' \
    -i jsonf \
    -t textf
```

```text
It's joker, help me aquaman!
It's reverseFlash, help me greenLantern!
It's ma'alefa'ak, help me batman!
```

Similar to `jsonf`, using `textf` here as our *template-processor* treats the `TEMPLATE` argument as a path to a text file. It opens the file, reads its contents; and passes the contents (as a Python str) to the renderer.

---

So far we've been using filters (e.g. `to_camel`, `to_pascal`, & `to_snake`) from the `CaseStyleExtension` which is loaded in by default, now let's try using filters from an extension from another package called `accelbyte_codegen.ext.py.jinja.PyExtension`.

```shell
./accelbyte-codegen render \
    '{"words": ["True", "False", "foo", "while", "for"]}' \
    '{% for word in words %}{{ word | python_class }} {{ word | python_variable }} {% endfor %}' \
    -i json \
    -t text \
    -e 'accelbyte_codegen.ext.py.jinja.PyExtension'
```

```text
True_ true False_ false Foo foo While while_ For for_
```

Here we've used the `python_class` and `python_variable` filters. These filters do additional work so that the resulting output does not match any of the Python reserved words (e.g. if, for, while, True, False, None).

---

Another variant of the `render` command is the `renderc` command, it takes in a yaml config file instead of individual arguments.

```shell
./accelbyte-codegen renderc --help
```

```text
Usage: accelbyte-codegen renderc [OPTIONS] CONFIG

Options:
  --input TEXT     Overrides 'input' value in the config file
  --template TEXT  Overrides 'template' value in the config file
  --help           Show this message and exit.
```

> :bulb: all argument paths are relative to the config file

---

Let's try it out.

```yaml
# data/config.yaml

input: characters.json
template: template1.j2
```

```shell
./accelbyte-codegen renderc data/config.yaml
```

```text
It's cheetah, help me superman!
It's reverseFlash, help me greenLantern!
It's blackManta, help me martianManhunter!
```

You can also use `--input` and/or `--template` to override the values.

```json5
// data/characters2.json

{
  "type": "Characters",
  "battle_cry": "Avengers, Assemble!",
  "superheroes": [
    "Black Widow",
    "Captain America",
    "Hawkeye",
    "Hulk",
    "Ironman",
    "Thor"
  ],
  "villains": [
    "Abomination",
    "Crossfire",
    "Iron Monger",
    "Loki",
    "Madame Hydra",
    "Red Skull"
  ]
}
```

```shell
./accelbyte-codegen renderc data/config.yaml \
    --input 'characters2.json'
```

```text
It's ironMonger, help me hulk!
It's madameHydra, help me hawkeye!
It's loki, help me thor!
```

```text
{# data/template2.j2 -#}

{{ superheroes[range(superheroes | count) | random] }}: {{ battle_cry }}
```

```shell
./accelbyte-codegen renderc data/config.yaml \
    --template 'template2.j2'
```

```text
Wonder Woman: Justice League, Advance!
```

```shell
./accelbyte-codegen renderc data/config.yaml \
    --input 'characters2.json' \
    --template 'template2.j2'
```

```text
Captain America: Avengers, Assemble!
```

---

This concludes this tutorial.

[Jinja]: https://jinja.palletsprojects.com
[Extensions]: https://jinja.palletsprojects.com/en/3.1.x/templates/#extensions
[Filters]: https://jinja.palletsprojects.com/en/3.1.x/templates/#filters
