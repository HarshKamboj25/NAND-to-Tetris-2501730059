#!/usr/bin/env python3
"""Two-pass assembler for the 16-bit Hack computer.

Usage:
    python assembler.py path/to/Program.asm
    python assembler.py path/to/Program.asm -o path/to/Program.hack

The K-dependent capstone feature for K=59 (K % 3 == 2) warns about
duplicate labels. The first definition is retained to avoid silently
changing previously resolved references.
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    **{f"R{i}": i for i in range(16)},
    "SCREEN": 16384, "KBD": 24576,
}
DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}
JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101",
}
SYMBOL_RE = re.compile(r"^[A-Za-z_.$:][\w.$:]*$")

class AssemblerError(Exception):
    pass

def clean_source(path: Path):
    """Return (source_line_number, cleaned_instruction) pairs."""
    result = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise AssemblerError(f"cannot read {path}: {exc}") from exc
    for line_no, raw in enumerate(lines, 1):
        code = raw.split("//", 1)[0]
        code = re.sub(r"\s+", "", code)
        if code:
            result.append((line_no, code))
    return result

def first_pass(lines):
    symbols = dict(PREDEFINED)
    rom_address = 0
    for line_no, instruction in lines:
        if instruction.startswith("(") and instruction.endswith(")"):
            label = instruction[1:-1]
            if not label or not SYMBOL_RE.match(label):
                raise AssemblerError(f"Line {line_no}: invalid label declaration {instruction!r}")
            if label in symbols:
                print(f"Warning: Line {line_no}: duplicate label '{label}' (first definition retained)", file=sys.stderr)
            else:
                symbols[label] = rom_address
        else:
            if instruction.startswith("(") or instruction.endswith(")"):
                raise AssemblerError(f"Line {line_no}: malformed label declaration")
            rom_address += 1
    if rom_address > 32768:
        raise AssemblerError("program exceeds the 32K ROM address space")
    return symbols

def encode_a(value: str, line_no: int, symbols: dict, next_variable: list[int]) -> str:
    token = value[1:]
    if not token:
        raise AssemblerError(f"Line {line_no}: missing A-instruction value")
    if token.isdigit():
        address = int(token)
    else:
        if not SYMBOL_RE.match(token):
            raise AssemblerError(f"Line {line_no}: invalid symbol {token!r}")
        if token not in symbols:
            symbols[token] = next_variable[0]
            next_variable[0] += 1
        address = symbols[token]
    if not 0 <= address <= 32767:
        raise AssemblerError(f"Line {line_no}: A-instruction value out of range: {address}")
    return format(address, "016b")

def encode_c(instruction: str, line_no: int) -> str:
    if instruction.count("=") > 1 or instruction.count(";") > 1:
        raise AssemblerError(f"Line {line_no}: invalid C-instruction")
    if "=" in instruction:
        dest, rest = instruction.split("=", 1)
    else:
        dest, rest = "", instruction
    if ";" in rest:
        comp, jump = rest.split(";", 1)
    else:
        comp, jump = rest, ""
    if dest not in DEST:
        raise AssemblerError(f"Line {line_no}: invalid destination {dest!r}")
    if comp not in COMP:
        raise AssemblerError(f"Line {line_no}: invalid computation {comp!r}")
    if jump not in JUMP:
        raise AssemblerError(f"Line {line_no}: invalid jump {jump!r}")
    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]

def assemble(source: Path):
    lines = clean_source(source)
    symbols = first_pass(lines)
    next_variable = [16]
    output = []
    for line_no, instruction in lines:
        if instruction.startswith("(") and instruction.endswith(")"):
            continue
        if instruction.startswith("@"):
            output.append(encode_a(instruction, line_no, symbols, next_variable))
        else:
            output.append(encode_c(instruction, line_no))
    return output, symbols

def main(argv=None):
    parser = argparse.ArgumentParser(description="Assemble Hack .asm source into 16-bit .hack machine code.")
    parser.add_argument("source", type=Path, help="input .asm file")
    parser.add_argument("-o", "--output", type=Path, help="output .hack file (default: same name)")
    args = parser.parse_args(argv)
    if args.source.suffix.lower() != ".asm":
        parser.error("input file must have .asm extension")
    try:
        machine_code, symbols = assemble(args.source)
        output_path = args.output or args.source.with_suffix(".hack")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("".join(line + "\n" for line in machine_code), encoding="utf-8")
        print(f"Assembled {len(machine_code)} instructions: {output_path}")
        print("Duplicate-label warning feature enabled (K=59, K mod 3=2).")
        return 0
    except AssemblerError as exc:
        print(f"Assembler error: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
