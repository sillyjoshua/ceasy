# Your first program

Create `hello.ceasy`:

```ceasy
# This is a comment
print("Hello, world!");
let year = 2026;
print(year);
```

Run it:

```bash
python3 ceasy.py hello.ceasy -o hello.c
gcc hello.c -o hello
./hello
```

## What each line means

- `# ...` is a Ceasy comment. The translator ignores it.
- `print("Hello, world!");` writes text followed by a newline.
- `let year = 2026;` declares a variable and infers its type from the value.
- `print(year);` displays the value of a declared variable.
- Semicolons end statements, as in C.

## Inspect the C

Open `hello.c` after translation. Learning to read the generated C is a useful way to understand what Ceasy does. The generated program has a `main` function and uses `printf` to display output.

## Try it

Change the message, change the number, then compile again. Make a copy of the file before experimenting if you want to keep your original example.