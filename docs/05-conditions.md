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

**Prototype limitation:** declarations and blocks are translated with minimal validation, and `print(...)` is currently handled by the translator's simple line-based rules. Nested blocks and complex conditions may not compile correctly. Check generated C before relying on a conditional program. Improving parsing and type checking is on the roadmap.