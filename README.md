# Ceasy

**C, without the intimidating first step.** Ceasy is a small, beginner-friendly, C-inspired language project. It uses readable commands such as `print("Hello!");` and `let score = 10;`.

> **Status: early prototype.** Ceasy includes a small Python-to-C transpiler, a standalone Windows double-click runtime build, and a full Markdown learning guide. The runtime supports a smaller subset than a complete programming language; see the documentation for exact limitations.

## Windows: double-click `.ce` and `.ceasy` files

1. Open the [Windows bundle workflow](https://github.com/sillyjoshua/ceasy/actions/workflows/build-windows.yml) and choose the latest successful run.
2. Download its `ceasy-windows` artifact and extract the ZIP to a permanent folder.
3. Double-click `install-windows.bat` once.
4. Create a `.ce` or `.ceasy` file and double-click it to run.

The bundle includes a standalone runtime, so Python and GCC are not required for the supported runtime syntax. Keep `ceasy.exe` in the folder where you extracted it. See [the full Windows setup guide](docs/13-double-click-windows.md).

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

## Learn Ceasy

Start with [`docs/00-start-here.md`](docs/00-start-here.md). The full guide lives in Markdown files under `docs/`:

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

## What works today

- `print(expression);` for supported strings, numbers, and variables
- `let name = expression;` with basic type inference in the transpiler
- A small standalone Windows runtime for double-clicking files
- `--check` to validate supported transpiler syntax
- `-o FILE` to choose generated C output

Ceasy is intentionally small. It does not yet implement a complete parser or every C feature. The double-click runtime and C transpiler have different supported syntax; consult the docs before relying on advanced control flow.

## Contributing

Issues and pull requests are welcome. Please include a small `.ceasy` example and expected behavior when proposing syntax changes. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first.

## License

MIT. See [`LICENSE`](LICENSE).