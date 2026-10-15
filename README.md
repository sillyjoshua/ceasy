# Ceasy

**C, without the intimidating first step.** Ceasy is a small, beginner-friendly, C-inspired language project. It uses readable commands such as `print("Hello!");` and `let score = 10;`.

> **Version 0.2.1.** Ceasy includes a small Python-to-C transpiler, a Windows double-click runtime, Minecraft-style 2D block graphics, Python-style imports of local `.cedev` addon source files, and `.cesecret` values that are redacted when printed directly.

## Windows: double-click `.ce` and `.ceasy` files

1. Open the [latest Ceasy release](https://github.com/sillyjoshua/ceasy/releases/latest) or the [Windows bundle workflow](https://github.com/sillyjoshua/ceasy/actions/workflows/build-windows.yml) and choose the latest successful run.
2. Download its `ceasy-windows` artifact and extract the ZIP to a permanent folder.
3. Double-click `install-windows.bat` once.
4. Create a `.ce` or `.ceasy` file and double-click it to run.

Keep `ceasy.exe` in the folder where you extracted it. The standalone runtime does not require you to install Python or GCC for supported syntax. See the [Windows setup guide](docs/13-double-click-windows.md).

## Make a block world

The runtime includes a tiny, beginner-friendly 2D block graphics system:

```ceasy
window("My Block World", 800, 600);
block(100, 300, "grass");
block(132, 300, "dirt");
block(164, 300, "stone");
player(200, 270);
text(20, 20, "Hello, block world!");
```

Run `examples/block-world.ceasy` to see a landscape and tree. Move the player with **WASD** or the **arrow keys**. Available blocks include grass, dirt, stone, sand, water, wood, planks, brick, leaves, bedrock, snow, gold, diamond and lava.

Read [Simple Minecraft-style graphics](docs/14-block-graphics.md) for the short guide. This is 2D block-building graphics, not a full 3D Minecraft engine. Graphics commands currently work in the double-click runtime and are not yet translated by the C transpiler.

## Python imports and addons

Ceasy supports regular Python-style imports in the double-click runtime:

```ceasy
import random;
let roll = random.randint(1, 6);
print(roll);
```

A `.cedev` file is a JSON addon source project. Put `gamifier.cedev` beside your program and use `import gamifier;` to load it—no installer or package installation is involved. See [Building and importing addons](docs/15-dev-addons.md) and the [Gamifier example](examples/gamifier-demo.ceasy).

## Secret values

Put values in a same-name `.cesecret` file beside your `.ceasy` file and access them with `secret("NAME")`. Directly printing a secret value shows `[secret]`, not the value. `.cesecret` is plain JSON, **not encrypted**; protect the file and never commit real credentials. See [Secret files](docs/16-secrets.md).

## Example

```ceasy
# My first Ceasy program
print("Hello, world!");
let score = 42;
print(score);
```

## Developer / transpiler quick start

For translating Ceasy source into C, Python 3.10+ and GCC or Clang are still required:

```bash
python3 ceasy.py examples/hello.ceasy -o hello.c
gcc hello.c -o hello
./hello
```

The transpiler and double-click runtime support different subsets of the language. Read the docs before relying on advanced syntax.

## Learn Ceasy

Start with [docs/00-start-here.md](docs/00-start-here.md). The learning guide is in Markdown under `docs/`:

1. [Installation](docs/01-installation.md)
2. [Your first program](docs/02-first-program.md)
3. [Variables and types](docs/03-variables-and-types.md)
4. [Input and output](docs/04-input-output.md)
5. [Conditions](docs/05-conditions.md)
6. [Loops](docs/06-loops.md)
7. [Functions and C interop](docs/07-functions-and-c.md)
8. [Errors and debugging](docs/08-errors-and-debugging.md)
9. [Language reference](docs/09-language-reference.md)
10. [Compiler internals](docs/10-compiler-internals.md)
11. [Exercises](docs/11-exercises.md)
12. [FAQ and roadmap](docs/12-faq-roadmap.md)
13. [Double-click Windows setup](docs/13-double-click-windows.md)
14. [Block graphics](docs/14-block-graphics.md)
15. [Addon projects](docs/15-dev-addons.md)
16. [Secret files](docs/16-secrets.md)

## Contributing

Issues and pull requests are welcome. Please include a small `.ceasy` example and expected behavior when proposing syntax changes. Read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## License

MIT. See [LICENSE](LICENSE).
