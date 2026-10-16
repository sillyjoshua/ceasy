# Conditions

Conditions let a program choose what to do. The current translator passes through a limited set of C-style control-flow lines, but this is an early feature and not a complete parser.

Example of the intended style:

```ceasy
let age = 16;
if (age >= 13) {
    print("Teenager or older");
}
```

Operators familiar from C include `==`, `!=`, `<`, `<=`, `>` and `>=`. Use `==` to compare values; a single `=` is assignment.

The standalone `.ce`/`.ceasy` interpreter supports `if` and `else` blocks, including nested conditions. Put the opening brace on the same line as the condition and use a separate closing brace:

```ceasy
let age = 13;
if (age >= 13) {
    print("teen yeah");
} else {
    print("not a teenager");
}
```

The C transpiler remains a separate, early feature with a limited parser; check generated C when using complex conditions or deeply nested code.