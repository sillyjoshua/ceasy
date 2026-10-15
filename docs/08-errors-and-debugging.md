# Errors and debugging

## Run the syntax checker

```bash
python3 ceasy.py examples/hello.ceasy --check
```

A successful check exits without output. An error is printed to the terminal and the command exits with a non-zero status.

## Common problems

- **Missing semicolon:** statements such as `print("Hi");` and `let n = 1;` need semicolons.
- **Unknown variable:** declare a variable before printing it.
- **Unsupported syntax:** check the exact subset in [Language reference](09-language-reference.md).
- **`gcc` not found:** install a C compiler and ensure it is on PATH.
- **Generated C fails to compile:** inspect the `.c` file. The prototype is intentionally limited, and some control-flow combinations are not supported yet.
- **A string has a typo:** use matching double quotes around text.

## Report a bug

Include your operating system, Python version, a minimal `.ceasy` example, the command you ran, the full error message and the generated C if it exists. Do not include passwords, tokens or private data.