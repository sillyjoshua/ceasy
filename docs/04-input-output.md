# Input and output

## Output with `print`

`print(expression);` prints a supported value followed by a newline.

```ceasy
print("Welcome!");
let points = 100;
print(points);
```

Supported arguments currently include quoted string literals, declared variables and simple numeric expressions. String concatenation and formatted multi-value output are not implemented.

## Reading input

Interactive input is not built into the current Ceasy prototype. Because Ceasy generates C, you can add C input functions in a future extended version, but this release's translator does not yet accept arbitrary C declarations or function calls. For now, use fixed values while learning variables and expressions.

## Newlines

Each `print` call adds a newline automatically. The string escape sequences accepted inside literals are passed to C, so `\n` in a C string represents a newline; prefer separate `print` calls for beginner examples.