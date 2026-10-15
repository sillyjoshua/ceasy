# Run `.ce` and `.ceasy` files by double-clicking (Windows)

Ceasy provides a standalone Windows runtime bundle so simple Ceasy programs can run without separately installing Python or GCC. GitHub Actions builds the bundle whenever the runtime files change.

## Download and set up once

1. Open the repository's [Actions page](https://github.com/sillyjoshua/ceasy/actions/workflows/build-windows.yml).
2. Open the latest successful **Build Windows double-click bundle** run.
3. Download the `ceasy-windows` artifact and extract the ZIP to a permanent folder, such as `Documents\\Ceasy`.
4. Double-click `install-windows.bat`. It registers `.ce` and `.ceasy` for your Windows user; administrator access should not be required.
5. Keep `ceasy.exe` in that folder. The registered file association points to it.

After setup, double-click a `.ce` or `.ceasy` file in File Explorer and its output appears in a console window. The console waits for Enter before closing.

## Example

Create `hello.ceasy` in Notepad and save it as **All files** (not Text Documents):

```ceasy
# Hello, Ceasy!
print("Hello, world!");
let answer = 6 * 7;
print(answer);
```

Double-click `hello.ceasy`. Expected output:

```text
Hello, world!
42
```

`.ce` and `.ceasy` use the same runtime.

## Current runtime limitations

The double-click runtime supports comments, `let` declarations, `print(...)`, basic numeric/string expressions and simple assignments. It does not yet execute `if`, `else`, `while`, `for`, custom functions, or arbitrary C code. Those are not silently claimed to work: the original `ceasy.py` transpiler remains available for generating C from the documented subset.

This is a per-user Windows file association. Linux and macOS need their own packaging and file-association setup. If Windows still opens Notepad, right-click a `.ceasy` file, choose **Open with**, and select the installed `ceasy.exe`.