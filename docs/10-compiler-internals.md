# Compiler internals

Ceasy currently uses a **transpiler**: it converts Ceasy source text into C source text. It does not generate machine code directly.

## Pipeline

1. Read a UTF-8 source file.
2. Split it into lines and ignore blank/comment lines.
3. Match supported declarations and `print` calls with regular expressions.
4. Track simple variable types to choose a C declaration and `printf` format.
5. Emit a C `main` function.
6. Optionally pass the generated C to GCC or Clang yourself.

## Code layout

- `ceasy.py` — command-line entry point, translator and basic diagnostics.
- `examples/` — small sample programs.
- `docs/` — language tutorial and reference.
- `tests/` — automated tests for supported syntax.

## Why keep it simple?

Regular expressions make a tiny prototype easy to read, but they are not suitable for a complete programming language. They struggle with nested expressions, scopes, escaped strings and nested blocks. A future version should tokenize input, parse it into an abstract syntax tree, validate types and then generate C from that tree.

## Running tests

```bash
python3 -m unittest discover -s tests -v
```

When adding a feature, add tests for valid syntax, invalid syntax and the generated C output.