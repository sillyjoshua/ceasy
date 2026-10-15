# Loops

Loops repeat work. Ceasy aims to retain familiar C-style `while` and `for` structures.

Intended example:

```ceasy
let count = 0;
while (count < 3) {
    print(count);
    count = count + 1;
}
```

A `while` loop repeats while its condition is true. A `for` loop is useful when you know how a counter starts, changes and stops.

**Prototype limitation:** the current translator only passes through a narrow subset of control-flow lines and does not yet understand indentation or nested scopes. It may not correctly translate `print` or `let` statements inside a block. Treat loop examples as learning goals rather than guaranteed-working compiler features until the parser is expanded.