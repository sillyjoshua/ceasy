#!/usr/bin/env python3
"""Small interpreter used for double-clicking .ce and .ceasy files."""
from __future__ import annotations
import ast
import operator
import re
import sys
from pathlib import Path

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv, ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod, ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos}

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
    raise RuntimeErrorCeasy("unsupported expression; try numbers, strings, variables, and + - * / parentheses")

def eval_expr(text: str, env: dict[str, object]) -> object:
    try:
        return expression(ast.parse(text, mode="eval").body, env)
    except (SyntaxError, ZeroDivisionError, TypeError, OverflowError) as exc:
        raise RuntimeErrorCeasy(f"invalid expression {text!r}: {exc}") from exc

def run_file(path: Path) -> None:
    env: dict[str, object] = {}
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        try:
            if line.endswith(";"):
                line = line[:-1].strip()
            if line.startswith("let "):
                match = re.fullmatch(r"let\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)", line)
                if not match:
                    raise RuntimeErrorCeasy("expected: let variable = expression;")
                name, value = match.groups()
                if name in env:
                    raise RuntimeErrorCeasy(f"variable {name!r} is already declared")
                env[name] = eval_expr(value, env)
            elif line.startswith("print(") and line.endswith(")"):
                print(eval_expr(line[6:-1], env))
            else:
                match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)\s*(=|\+=|-=|\*=|/=)\s*(.+)", line)
                if not match:
                    raise RuntimeErrorCeasy("this double-click runner currently supports let, print, and simple assignments; see docs/13-double-click-windows.md")
                name, op, value = match.groups()
                if name not in env:
                    raise RuntimeErrorCeasy(f"unknown variable {name!r}; declare it with let first")
                right = eval_expr(value, env)
                if op == "=": env[name] = right
                elif op == "+=": env[name] += right
                elif op == "-=": env[name] -= right
                elif op == "*=": env[name] *= right
                elif op == "/=": env[name] /= right
        except (RuntimeErrorCeasy, ZeroDivisionError, TypeError, ValueError) as exc:
            raise RuntimeErrorCeasy(f"{path.name}:{number}: {exc}") from exc

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
    if pause:
        input("\nProgram finished. Press Enter to close...")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())