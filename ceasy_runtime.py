#!/usr/bin/env python3
"""Small interpreter for Ceasy .ce/.ceasy programs and .cedev addon projects."""
from __future__ import annotations
import ast
import builtins
import importlib
import json
import math
import random
import statistics
import datetime
import time
import decimal
import types
import operator
import re
import shutil
import subprocess
import sys
from pathlib import Path

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
       ast.Mod: operator.mod, ast.Pow: operator.pow, ast.USub: operator.neg,
       ast.UAdd: operator.pos}

class RuntimeErrorCeasy(Exception):
    """A readable error from the Ceasy runtime."""

class SecretValue(str):
    """A string value whose normal display is redacted."""
    def __str__(self) -> str:
        return "[secret]"
    def __repr__(self) -> str:
        return "SecretValue('[secret]')"

def expression(node: ast.AST, env: dict[str, object]) -> object:
    allowed = (ast.Expression, ast.Constant, ast.Name, ast.BinOp, ast.UnaryOp,
               ast.BoolOp, ast.And, ast.Or, ast.Compare, ast.Eq, ast.NotEq,
               ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn, ast.Is,
               ast.IsNot, ast.IfExp, ast.List, ast.Tuple, ast.Dict, ast.Attribute,
               ast.Call, ast.Subscript, ast.Slice, ast.Load, ast.Add, ast.Sub,
               ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow, ast.USub,
               ast.UAdd, ast.Not, ast.UnaryOp)
    for item in ast.walk(node):
        if not isinstance(item, allowed):
            raise RuntimeErrorCeasy("unsupported expression; use values, arithmetic, imports and function calls")
        if isinstance(item, ast.Attribute) and item.attr.startswith("_"):
            raise RuntimeErrorCeasy("private/dunder attributes are not available in Ceasy")
        if isinstance(item, ast.Name) and item.id.startswith("__"):
            raise RuntimeErrorCeasy("private/dunder names are not available in Ceasy")
        if isinstance(item, ast.Call) and item.keywords:
            raise RuntimeErrorCeasy("use positional arguments in function calls")
    try:
        return eval(compile(ast.Expression(node), "<ceasy>", "eval"), {"__builtins__": {}}, env)
    except (NameError, AttributeError, TypeError, ValueError, ZeroDivisionError, OverflowError, KeyError, IndexError) as exc:
        raise RuntimeErrorCeasy(f"invalid expression: {exc}") from exc

def eval_expr(text: str, env: dict[str, object]) -> object:
    try:
        return expression(ast.parse(text, mode="eval").body, env)
    except SyntaxError as exc:
        raise RuntimeErrorCeasy(f"invalid expression {text!r}: {exc}") from exc

def call_args(line: str, env: dict[str, object]) -> tuple[str, list[object]]:
    match = re.fullmatch(r"([A-Za-z_]\w*)\s*\((.*)\)", line, re.S)
    if not match:
        raise RuntimeErrorCeasy("expected a function-style command, e.g. block(64, 64, \"grass\")")
    name, raw = match.groups()
    try:
        parsed = ast.parse(f"f({raw})", mode="eval").body
    except SyntaxError as exc:
        raise RuntimeErrorCeasy(f"invalid arguments: {exc}") from exc
    if not isinstance(parsed, ast.Call) or parsed.keywords:
        raise RuntimeErrorCeasy("use positional arguments only")
    return name, [expression(arg, env) for arg in parsed.args]

def load_secrets(path: Path) -> dict[str, SecretValue]:
    secret_path = path.with_suffix(".cesecret")
    if not secret_path.exists():
        return {}
    try:
        data = json.loads(secret_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeErrorCeasy(f"could not load {secret_path.name}: expected a JSON object") from exc
    if not isinstance(data, dict) or not all(isinstance(k, str) and isinstance(v, (str, int, float, bool)) for k, v in data.items()):
        raise RuntimeErrorCeasy(f"{secret_path.name} must contain a JSON object of simple values")
    return {key: SecretValue(str(value)) for key, value in data.items()}

def load_addon(path: Path, expected_name: str, cache: dict[str, object]) -> object:
    """Load a local .cedev addon project as an importable Python-backed module."""
    try:
        config = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeErrorCeasy(f"{path.name} must be a valid JSON .cedev addon project") from exc
    if not isinstance(config, dict):
        raise RuntimeErrorCeasy(".cedev addon must contain a JSON object")
    name = config.get("name", path.stem)
    source = config.get("source", "")
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z_]\w*", name):
        raise RuntimeErrorCeasy(".cedev 'name' must be a valid module name")
    if name != expected_name or path.stem != expected_name:
        raise RuntimeErrorCeasy(f"addon name must match its filename: {expected_name}.cedev")
    if not isinstance(source, str) or not source.strip():
        raise RuntimeErrorCeasy(f"{path.name} needs a non-empty Python 'source' string")
    module = types.ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ""
    cache[name] = module
    try:
        exec(compile(source, str(path), "exec"), module.__dict__)
    except Exception as exc:
        cache.pop(name, None)
        raise RuntimeErrorCeasy(f"could not load addon {name!r}: {exc}") from exc
    return module


def load_import(module_name: str, directory: Path, cache: dict[str, object]) -> object:
    """Prefer a sibling .cedev addon; otherwise use an installed Python module."""
    if module_name in cache:
        return cache[module_name]
    if re.fullmatch(r"[A-Za-z_]\w*", module_name):
        addon_path = directory / f"{module_name}.cedev"
        if addon_path.is_file():
            return load_addon(addon_path, module_name, cache)
    return importlib.import_module(module_name)

def show_game(title: str, width: int, height: int, blocks: list[tuple[int, int, str, int]], texts: list[tuple[int, int, str]], player: list[int] | None) -> None:
    try:
        import tkinter as tk
    except ImportError as exc:
        raise RuntimeErrorCeasy("graphics need Python's Tk support; on Windows, use the official Windows bundle") from exc
    colours = {
        "grass": ("#69a843", "#477d30"), "dirt": ("#986438", "#704525"),
        "stone": ("#92989b", "#696f72"), "sand": ("#e4d08a", "#b9a766"),
        "water": ("#399fe0", "#2475b0"), "wood": ("#a87543", "#77502e"),
        "planks": ("#c08b54", "#8c6239"), "brick": ("#b85b4a", "#873e34"),
        "leaves": ("#32834a", "#215d34"), "bedrock": ("#41464b", "#222629"),
        "snow": ("#f2f5f5", "#c8d1d4"), "gold": ("#f4c542", "#b98a20"),
        "diamond": ("#54e1d0", "#2a9c94"), "lava": ("#ff7a24", "#c94516"),
    }
    root = tk.Tk()
    root.title(title)
    canvas = tk.Canvas(root, width=width, height=height, bg="#87c9f5", highlightthickness=0)
    canvas.pack()
    canvas.create_rectangle(0, int(height * .72), width, height, fill="#83bd57", outline="")
    for x, y, kind, size in blocks:
        if kind not in colours:
            raise RuntimeErrorCeasy(f"unknown block {kind!r}; try grass, dirt, stone, sand, water, wood, planks, brick, leaves, bedrock, snow, gold, diamond or lava")
        main, shade = colours[kind]
        canvas.create_rectangle(x, y, x + size, y + size, fill=main, outline=shade, width=2)
        canvas.create_rectangle(x + 4, y + 4, x + size // 3, y + 7, fill="#ffffff", outline="")
        if kind in ("grass", "dirt", "stone", "sand", "bedrock"):
            canvas.create_rectangle(x + size * .62, y + size * .58, x + size * .78, y + size * .68, fill=shade, outline="")
    for x, y, message in texts:
        canvas.create_text(x, y, text=message, fill="#18212a", font=("Consolas", 14, "bold"), anchor="nw")
    if player is not None:
        px, py = player
        body = canvas.create_rectangle(px, py, px + 22, py + 28, fill="#4b77d1", outline="#24427c", width=2)
        face = canvas.create_rectangle(px + 3, py + 3, px + 19, py + 13, fill="#f0c49b", outline="")
        def move(dx: int, dy: int) -> None:
            canvas.move(body, dx, dy)
            canvas.move(face, dx, dy)
        root.bind("<Left>", lambda _e: move(-8, 0)); root.bind("<Right>", lambda _e: move(8, 0))
        root.bind("<Up>", lambda _e: move(0, -8)); root.bind("<Down>", lambda _e: move(0, 8))
        root.bind("<KeyPress-a>", lambda _e: move(-8, 0)); root.bind("<KeyPress-d>", lambda _e: move(8, 0))
        root.bind("<KeyPress-w>", lambda _e: move(0, -8)); root.bind("<KeyPress-s>", lambda _e: move(0, 8))
    root.mainloop()

def add_external_site_packages() -> None:
    """Let a frozen Windows runtime see packages installed by .cedev using system Python."""
    if not getattr(sys, "frozen", False):
        return
    python = shutil.which("python") or shutil.which("py")
    if not python:
        return
    try:
        output = subprocess.check_output(
            [python, "-c", "import site; print('\n'.join(site.getsitepackages() + [site.getusersitepackages()]))"],
            text=True, stderr=subprocess.DEVNULL, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return
    for entry in output.splitlines():
        if entry and Path(entry).is_dir() and entry not in sys.path:
            sys.path.append(entry)

def run_file(path: Path) -> None:
    add_external_site_packages()
    env: dict[str, object] = {}
    addon_cache: dict[str, object] = {}
    secrets = load_secrets(path)
    def secret(name: str) -> SecretValue:
        if name not in secrets:
            raise RuntimeErrorCeasy(f"secret {name!r} was not found in {path.with_suffix('.cesecret').name}")
        return secrets[name]
    def safe_print(*values: object, sep: str = " ", end: str = "\n") -> None:
        rendered = sep.join(str(value) for value in values)
        for value in secrets.values():
            raw = str.__str__(value)
            if raw:
                rendered = rendered.replace(raw, "[secret]")
        builtins.print(rendered, end=end)
    env.update({"secret": secret, "print": safe_print})
    window: tuple[str, int, int] | None = None
    blocks: list[tuple[int, int, str, int]] = []
    texts: list[tuple[int, int, str]] = []
    player: list[int] | None = None
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        if line.endswith(";"):
            line = line[:-1].strip()
        try:
            import_match = re.fullmatch(r"import\s+([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)(?:\s+as\s+([A-Za-z_]\w*))?", line)
            from_match = re.fullmatch(r"from\s+([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)\s+import\s+([A-Za-z_]\w*)(?:\s+as\s+([A-Za-z_]\w*))?", line)
            if import_match:
                module_name, alias = import_match.groups()
                module = load_import(module_name, path.parent, addon_cache)
                if alias or "." not in module_name:
                    env[alias or module_name] = module
                else:
                    env[module_name.split(".")[0]] = importlib.import_module(module_name.split(".")[0])
                continue
            if from_match:
                module_name, member, alias = from_match.groups()
                module = load_import(module_name, path.parent, addon_cache)
                if member.startswith("_") or not hasattr(module, member):
                    raise RuntimeErrorCeasy(f"{member!r} is not available from {module_name}")
                env[alias or member] = getattr(module, member)
                continue
            if line.startswith("let "):
                match = re.fullmatch(r"let\s+([A-Za-z_]\w*)\s*=\s*(.+)", line, re.S)
                if not match:
                    raise RuntimeErrorCeasy("expected: let name = expression;")
                name, value = match.groups()
                if name in env and name not in ("secret", "print"):
                    raise RuntimeErrorCeasy(f"variable {name!r} is already declared")
                env[name] = eval_expr(value, env)
                continue
            if line.startswith("print(") and line.endswith(")"):
                safe_print(eval_expr(line[6:-1], env))
                continue
            if re.match(r"[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*\s*\(", line):
                if "." in line.split("(", 1)[0]:
                    eval_expr(line, env)
                    continue
                name, args = call_args(line, env)
                if name == "window" and len(args) == 3:
                    window = (str(args[0]), int(args[1]), int(args[2]))
                elif name == "block" and len(args) in (3, 4):
                    x, y, kind = int(args[0]), int(args[1]), str(args[2]).lower()
                    size = int(args[3]) if len(args) == 4 else 32
                    if size < 8 or size > 128:
                        raise RuntimeErrorCeasy("block size must be between 8 and 128")
                    blocks.append((x, y, kind, size))
                elif name == "player" and len(args) == 2:
                    player = [int(args[0]), int(args[1])]
                elif name == "text" and len(args) == 3:
                    texts.append((int(args[0]), int(args[1]), str(args[2])))
                elif name in env and callable(env[name]):
                    env[name](*args)
                else:
                    raise RuntimeErrorCeasy("supported commands: imported addon functions, window, block, player and text")
                continue
            match = re.fullmatch(r"([A-Za-z_]\w*)\s*(\+=|-=|\*=|/=|=)\s*(.+)", line, re.S)
            if not match:
                raise RuntimeErrorCeasy("supported commands: import, from ... import, let, print, graphics and simple assignments")
            name, op, rhs = match.groups()
            if name not in env:
                raise RuntimeErrorCeasy(f"unknown variable {name!r}; declare it with let first")
            value = eval_expr(rhs, env)
            if op == "=": env[name] = value
            elif op == "+=": env[name] += value
            elif op == "-=": env[name] -= value
            elif op == "*=": env[name] *= value
            elif op == "/=": env[name] /= value
        except (RuntimeErrorCeasy, ValueError, TypeError, OverflowError, ImportError) as exc:
            raise RuntimeErrorCeasy(f"{path.name}:{number}: {exc}") from exc
    if window is not None:
        title, width, height = window
        if not 160 <= width <= 1920 or not 120 <= height <= 1080:
            raise RuntimeErrorCeasy("window size must be 160–1920 wide and 120–1080 high")
        show_game(title, width, height, blocks, texts, player)
    elif blocks or texts or player is not None:
        raise RuntimeErrorCeasy("add window(\"My Block Game\", 800, 600); before graphics commands")

def main() -> int:
    args = [arg for arg in sys.argv[1:] if arg != "--pause"]
    pause = "--pause" in sys.argv[1:]
    if not args:
        print("Ceasy: drag a .ce or .ceasy file onto this program, or open a source file.")
        return 2
    path = Path(args[0])
    try:
        if path.suffix.lower() == ".cedev":
            raise RuntimeErrorCeasy(".cedev files are addon projects, not programs. Import one from a .ceasy file with: import " + path.stem + ";")
        run_file(path)
        result = 0
    except (OSError, RuntimeErrorCeasy) as exc:
        print(f"Ceasy error: {exc}", file=sys.stderr)
        if pause:
            input("\nPress Enter to close...")
        return 1
    if pause and path.suffix.lower() != ".ceasy" and path.suffix.lower() != ".ce":
        input("\nFinished. Press Enter to close...")
    return result

if __name__ == "__main__":
    raise SystemExit(main())
