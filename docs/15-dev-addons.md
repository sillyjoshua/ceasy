# Building and importing `.cedev` addons

A `.cedev` file is an **addon project/source file**, not an installer. Ceasy does not install packages when you open it. Instead, save an addon such as `gamifier.cedev` beside your `.ceasy` program and import it by filename:

```ceasy
import gamifier;
gamifier.start("My Game");
gamifier.action("Finished my first task", 20);
```

## Addon file format

A `.cedev` file is JSON with addon metadata and a `source` field containing Python code. Ceasy loads that source as an importable module when it sees `import <name>;` or `from <name> import <function>;`. The `name` must match the file name without `.cedev`.

```json
{
  "name": "hello_addon",
  "version": "1.0.0",
  "description": "A tiny example addon",
  "source": "def greet(name):\n    print('Hello, ' + str(name))\n"
}
```

Save it as `hello_addon.cedev`, then use it from `app.ceasy`:

```ceasy
import hello_addon;
hello_addon.greet("Ceasy");
```

You can put the addon source directly in the JSON `source` string, escaping newlines as `\n`. The `examples/gamifier.cedev` file is a complete working addon and `examples/gamifier-demo.ceasy` shows how to use it.

## Important security note

Addon `source` is Python code and runs with your user's permissions when imported. Only import `.cedev` files you trust. A `.cedev` addon does not install Python packages, and there is no package installation step.

This local `.cedev` import feature is supported by the double-click runtime. The C transpiler (`ceasy.py`) does not currently execute Python-backed addons.
