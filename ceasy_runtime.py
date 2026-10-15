#!/usr/bin/env python3
"""Small interpreter for double-clickable .ce and .ceasy programs."""
from __future__ import annotations
import ast
import operator
import re
import sys
from pathlib import Path

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
       ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv,
       ast.Mod: operator.mod, ast.Pow: operator.pow,
       ast.USub: operator.neg, ast.UAdd: operator.pos}

class RuntimeErrorCeasy(Exception):
    pass

def expression(node: ast.AST, env: dict[str, object]) -> object:
    if isinstance(node, ast.Constant) and isinstance(node.value, (str, int, float, bool)):
        return node.value
    if isinstance(node, ast.Name):
        if node.id not in env:
            raise RuntimeErrorCeasy(f"unknown variable {node.id!r}")
        return env[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        return OPS[type(node.op)](expression(node.left, env), expression(node.right, env))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](expression(node.operand, env))
    raise RuntimeErrorCeasy("unsupported expression; use strings, numbers, variables and basic arithmetic")

def eval_expr(text: str, env: dict[str, object]) -> object:
    try:
        return expression(ast.parse(text, mode="eval").body, env)
    except (SyntaxError, ZeroDivisionError, TypeError, ValueError, OverflowError) as exc:
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

def show_game(title: str, width: int, height: int, blocks: list[tuple[int, int, str, int]], texts: list[tuple[int, int, str]], player: list[int] | None) -> None:
    try:
        import tkinter as tk
    except ImportError as exc:
        raise RuntimeErrorCeasy("graphics need Python's Tk support; on Windows, reinstall Python with Tcl/Tk, or download the official Windows bundle") from exc
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
    # A simple grass horizon gives a game-like scene without extra setup.
    canvas.create_rectangle(0, int(height * .72), width, height, fill="#83bd57", outline="")
    for x, y, kind, size in blocks:
        if kind not in colours:
            raise RuntimeErrorCeasy(f"unknown block {kind!r}; try grass, dirt, stone, sand, water, wood, planks, brick, leaves, bedrock, snow, gold, diamond or lava")
        main, shade = colours[kind]
        canvas.create_rectangle(x, y, x + size, y + size, fill=main, outline=shade, width=2)
        # Tiny pixel highlights make the blocks look chunky, not flat.
        canvas.create_rectangle(x + 4, y + 4, x + size // 3, y + 7, fill="#ffffff", outline="")
        if kind in ("grass", "dirt", "stone", "sand", "bedrock"):
            canvas.create_rectangle(x + size * .62, y + size * .58, x + size * .78, y + size * .68, fill=shade, outline="")
    for x, y, message in texts:
        canvas.create_text(x, y, text=message, fill="#18212a", font=("Consolas", 14, "bold"), anchor="nw")
    if player is not None:
        px, py = player
        body = canvas.create_rectangle(px, py, px + 22, py + 28, fill="#4b77d1", outline="#24427c", width=2)
        canvas.create_rectangle(px + 3, py + 3, px + 19, py + 13, fill="#f0c49b", outline="")
        # Keyboard movement: WASD or arrows.
        def move(dx: int, dy: int) -> None:
            canvas.move(body, dx, dy)
            for item in canvas.find_all()[-2:]:
                if item != body:
                    canvas.move(item, dx, dy)
        root.bind("<Left>", lambda _e: move(-8, 0)); root.bind("<Right>", lambda _e: move(8, 0))
        root.bind("<Up>", lambda _e: move(0, -8)); root.bind("<Down>", lambda _e: move(0, 8))
        root.bind("<KeyPress-a>", lambda _e: move(-8, 0)); root.bind("<KeyPress-d>", lambda _e: move(8, 0))
        root.bind("<KeyPress-w>", lambda _e: move(0, -8)); root.bind("<KeyPress-s>", lambda _e: move(0, 8))
    root.mainloop()

def run_file(path: Path) -> None:
    env: dict[str, object] = {}
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
            if line.startswith("let "):
                match = re.fullmatch(r"let\s+([A-Za-z_]\w*)\s*=\s*(.+)", line, re.S)
                if not match:
                    raise RuntimeErrorCeasy("expected: let name = expression;")
                name, value = match.groups()
                if name in env:
                    raise RuntimeErrorCeasy(f"variable {name!r} is already declared")
                env[name] = eval_expr(value, env)
                continue
            if line.startswith("print(") and line.endswith(")"):
                print(eval_expr(line[6:-1], env))
                continue
            if re.match(r"[A-Za-z_]\w*\s*\(", line):
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
                else:
                    raise RuntimeErrorCeasy("supported graphics commands: window(title, width, height), block(x, y, type[, size]), player(x, y), text(x, y, message)")
                continue
            match = re.fullmatch(r"([A-Za-z_]\w*)\s*(\+=|-=|\*=|/=|=)\s*(.+)", line, re.S)
            if not match:
                raise RuntimeErrorCeasy("supported commands: let, print, window, block, player, text and simple assignments")
            name, op, rhs = match.groups()
            if name not in env:
                raise RuntimeErrorCeasy(f"unknown variable {name!r}; declare it with let first")
            value = eval_expr(rhs, env)
            if op == "=": env[name] = value
            elif op == "+=": env[name] += value
            elif op == "-=": env[name] -= value
            elif op == "*=": env[name] *= value
            elif op == "/=": env[name] /= value
        except (RuntimeErrorCeasy, ValueError, TypeError, OverflowError) as exc:
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
        run_file(path)
    except (OSError, RuntimeErrorCeasy) as exc:
        print(f"Ceasy error: {exc}", file=sys.stderr)
        if pause:
            input("\nPress Enter to close...")
        return 1
    if pause and not any(arg in ("window(",) for arg in []):
        input("\nProgram finished. Press Enter to close...")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
