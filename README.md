# Ceasy

**C, without the intimidating first step.** Ceasy is a small, beginner-friendly, C-inspired language project. It uses readable commands such as `print("Hello!");` and `let score = 10;`, then translates supported Ceasy code into C.

> **Status: early prototype.** This repository includes a small Python transpiler and a learning guide. It is not a replacement for C, and the current compiler supports only the subset documented here.

## Quick start

Requirements: Python 3.10+ and a C compiler such as GCC or Clang.

```bash
python3 ceasy.py examples/hello.ceasy -o hello.c
gcc hello.c -o hello
./hello
```

On Windows, run `py ceasy.py examples/hello.ceasy -o hello.c`, then compile `hello.c` with GCC/Clang (for example, through MinGW-w64).

Example program (`examples/hello.ceasy`):

```ceasy
# My first Ceasy program
print("Hello, world!");
let score = 42;
print(score);
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

## What works today

- `print(expression);` for string literals and simple numeric expressions/variables
- `let name = expression;` with basic type inference for integer, decimal and string literals
- C-style comments (`// ...`) and Ceasy comments (`# ...`)
- A limited subset of C-style control-flow lines; see the reference for limitations
- `--check` to validate supported syntax without writing output
- `-o FILE` to choose generated C output

The prototype is intentionally small. It does not yet implement a full parser or every C feature.

## Contributing

Issues and pull requests are welcome. Please include a small `.ceasy` example and expected generated C when proposing syntax changes. Read [`CONTRIBUTING.md`](CONTRIBUTING.md) first.

## License

MIT. See [`LICENSE`](LICENSE).