#!/usr/bin/env python3
"""Ceasy prototype: translate a small beginner-friendly syntax subset to C."""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

IDENT = r"[A-Za-z_][A-Za-z0-9_]*"
LET_RE = re.compile(rf"^let\s+({IDENT})\s*=\s*(.+);$")
PRINT_RE = re.compile(r"^print\((.*)\);$")
INT_RE = re.compile(r"^-?(?:0|[1-9][0-9]*)$")
FLOAT_RE = re.compile(r"^-?(?:[0-9]+\.[0-9]+)$")
STRING_RE = re.compile(r'^"(?:[^"\\]|\\.)*"$')

class CeasyError(Exception):
    """A user-facing source translation error."""

def infer(value: str) -> str:
    value = value.strip()
    if STRING_RE.fullmatch(value):
        return "char *"
    if INT_RE.fullmatch(value):
        return "int"
    if FLOAT_RE.fullmatch(value):
        return "double"
    if re.fullmatch(IDENT, value):
        return "inferred"
    if re.fullmatch(r"[0-9+*/(). \-]+", value) and any(ch.isdigit() for ch in value):
        return "double" if "." in value else "int"
    raise CeasyError(f"can't infer the type of {value!r}; use a string, number, or existing variable")

def compile_source(source: str, filename: str = "<input>") -> str:
    out = ["#include <stdio.h>", "#include <stdbool.h>", "", "int main(void) {"]
    variables: dict[str, str] = {}
    for number, raw in enumerate(source.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("//"):
            continue
        if line in ("{", "}", "else {", "else", "};") or line.startswith(("if ", "if(", "while ", "while(", "for ", "for(")):
            out.append("    " + line)
            continue
        let_match = LET_RE.fullmatch(line)
        if let_match:
            name, value = let_match.groups()
            if name in variables:
                raise CeasyError(f"{filename}:{number}: variable {name!r} is already declared")
            kind = infer(value)
            if kind == "inferred":
                ref = value.strip()
                if ref not in variables:
                    raise CeasyError(f"{filename}:{number}: unknown variable {ref!r}")
                kind = variables[ref]
            variables[name] = kind
            out.append(f"    {kind} {name} = {value};")
            continue
        print_match = PRINT_RE.fullmatch(line)
        if print_match:
            value = print_match.group(1).strip()
            if STRING_RE.fullmatch(value):
                out.append(f"    printf(\"%s\\n\", {value});")
            elif re.fullmatch(IDENT, value) and value in variables:
                kind = variables[value]
                fmt = "%s" if kind == "char *" else ("%f" if kind == "double" else "%d")
                out.append(f"    printf(\"{fmt}\\n\", {value});")
            else:
                kind = infer(value)
                if kind not in ("int", "double"):
                    raise CeasyError(f"{filename}:{number}: print() supports string literals, numeric expressions, and declared variables")
                fmt = "%f" if kind == "double" else "%d"
                out.append(f"    printf(\"{fmt}\\n\", {value});")
            continue
        if line.startswith("#include") or line.startswith("return "):
            out.append("    " + line)
            continue
        if line.endswith(";") and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*\s*(?:=|\+=|-=|\*=|/=).*;", line):
            out.append("    " + line)
            continue
        raise CeasyError(f"{filename}:{number}: unsupported syntax: {line!r}. See docs/09-language-reference.md")
    out.extend(["    return 0;", "}", ""])
    return "\n".join(out)

def main() -> int:
    parser = argparse.ArgumentParser(description="Compile the supported Ceasy subset to C")
    parser.add_argument("source", help="input .ceasy file")
    parser.add_argument("-o", "--output", help="output C file (default: stdout)")
    parser.add_argument("--check", action="store_true", help="check syntax without writing generated C")
    args = parser.parse_args()
    path = Path(args.source)
    try:
        result = compile_source(path.read_text(encoding="utf-8"), str(path))
        if not args.check:
            if args.output:
                Path(args.output).write_text(result, encoding="utf-8")
            else:
                sys.stdout.write(result)
    except (OSError, CeasyError) as exc:
        print(f"ceasy: error: {exc}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())