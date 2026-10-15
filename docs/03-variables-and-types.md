# Variables and types

A variable gives a name to a value.

```ceasy
let lives = 3;
let temperature = 18.5;
let username = "josh";
print(lives);
print(temperature);
print(username);
```

The prototype infers a basic C type from the initial value:

| Ceasy value | Generated C type | Example |
|---|---|---|
| Whole number | `int` | `let lives = 3;` |
| Decimal number | `double` | `let temperature = 18.5;` |
| Quoted text | `char *` | `let username = "josh";` |

Names may contain letters, digits and underscores, but cannot start with a digit. Names are case-sensitive. `score` and `Score` are different names.

## Reassignment

The prototype allows simple reassignment statements such as `lives = 2;`, but currently does not perform complete type checking for assignments. Keep the new value compatible with the original type.

## Arithmetic

Integer and decimal arithmetic can use `+`, `-`, `*`, `/` and parentheses:

```ceasy
let total = 10 + 5 * 2;
print(total);
let average = (10 + 5) / 2.0;
print(average);
```

C precedence rules apply. In the current prototype, arithmetic expressions are deliberately limited to numeric literals and operators; full expression parsing is planned work.