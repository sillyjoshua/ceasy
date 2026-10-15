# Installation

## Requirements

- Python 3.10 or newer
- GCC or Clang to compile generated C
- Git is optional if you download the repository as a ZIP

## Get the code

```bash
git clone https://github.com/sillyjoshua/ceasy.git
cd ceasy
```

## Check Python

```bash
python3 --version
```

On Windows, try `py --version`.

## Check a C compiler

```bash
gcc --version
```

If GCC is not installed, install a compiler appropriate for your operating system. On Ubuntu/Debian, `sudo apt install build-essential` installs GCC and common build tools. On macOS, install Apple's command-line developer tools with `xcode-select --install`. On Windows, install a GCC distribution such as MinGW-w64 and ensure its `bin` directory is on PATH.

## Compile the example

Linux/macOS:

```bash
python3 ceasy.py examples/hello.ceasy -o hello.c
gcc hello.c -o hello
./hello
```

Windows PowerShell:

```powershell
py ceasy.py examples/hello.ceasy -o hello.c
gcc hello.c -o hello.exe
.\hello.exe
```

Expected output:

```text
Hello, world!
42
```

If `gcc` is not recognised, the C compiler is missing or its path is not configured. If Python cannot be found, use the command name configured by your installation.