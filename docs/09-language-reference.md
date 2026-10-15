# Ceasy language reference (prototype)

This document describes the implementation as it currently exists, not every planned feature.

## Comments and blank lines

- Lines beginning with `#` are comments.
- Lines beginning with `//` are comments.
- Blank lines are ignored.

Comments are currently recognized only when they begin the line after whitespace trimming; inline comments are not supported.

## Declarations

```ceasy
let count = 10;
let ratio = 2.5;
let message = "hello";
```

`let IDENTIFIER = VALUE;` supports a quoted string, integer, decimal or limited numeric expression. A declaration name may only be declared once in the source file. Type inference is basic, not a full static type system.

## Output

```ceasy
print("hello");
let count = 10;
print(count);
print(2 + 3);
```

The translator supports string literals, declared variables and simple numeric expressions. Printing a variable uses the type inferred when it was declared.

## Reassignment

Simple assignments like `count = 12;` are passed through to C. Type correctness is left to the C compiler.

## Control flow

A limited number of C-style lines (`if (...) {`, `while (...) {`, `for (...) {`, `else {`, `{` and `}`) are passed through. Complex/nested control flow is not a reliable supported feature yet.

## Generated program

The translator wraps output in `int main(void)`, includes `stdio.h` and `stdbool.h`, and returns zero. It does not support custom functions, imports, arrays, structs, pointers as Ceasy syntax, user-defined types, classes, packages or a runtime library.

## CLI

```text
python3 ceasy.py SOURCE [-o OUTPUT] [--check]
```

- `SOURCE`: path to a UTF-8 `.ceasy` file.
- `-o`, `--output`: write generated C to this path. Without it, generated C goes to standard output.
- `--check`: translate to validate the supported syntax, but do not write generated C.

## Grammar sketch

```text
program        := line*
line           := comment | declaration | print_statement | supported_c_line | assignment
declaration    := "let" identifier "=" expression ";"
print_statement := "print(" expression ");"
```

This is a sketch, not a formal complete grammar. The actual implementation is line-based and has stricter rules than a full language parser.