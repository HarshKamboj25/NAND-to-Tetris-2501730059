# Nand to Tetris Capstone: Make the Computer Draw a Box

**Student:** Harsh Kamboj  
**Roll Number:** 2501730059  
**K:** 59  
**Course:** Nand to Tetris – I (ETCCNT301)  
**University:** K.R. Mangalam University

## K-Dependent Configuration

- K = 59; K mod 3 = 2
- Custom assembler feature: duplicate-label warning
- Starting screen row: 59
- Box height: 20 rows
- Box width: 64 pixels (4 Hack screen words)
- First screen address: 16384 + (32 × 59) = 18272

## Project Files

- `CPU.hdl`: Hack CPU implementation.
- `Memory.hdl`: RAM, Screen and Keyboard integration.
- `Computer.hdl`: Complete Hack computer.
- `assembler.py`: Custom two-pass Hack assembler.
- `Box.asm`: Keyboard-controlled rectangle program.
- `Box.hack`: Generated machine code.
- `tests/`: Python unit tests.
- `test_programs/`: Assembler test programs.
- `test_results/`: Local unit-test results.
- `docs/`: Capstone report.

The Viva Guide is stored separately outside this project folder. `audit_temp/` contains temporary verification files and the original README backup; exclude it from the final submission.

## Assemble the Program

Run in PowerShell from the project directory:

```powershell
python .\assembler.py .\Box.asm
```

To specify an output path:

```powershell
python .\assembler.py .\Box.asm -o .\Box.hack
```

## Box Program

The program draws a 64-pixel-wide, 20-row-high rectangle beginning at screen row 59. It writes four screen words per row. While a key is pressed, it draws the rectangle in black; when no key is pressed, it clears the same rectangle. The program continuously redraws the rectangle.

## Local Verification Completed

Command used:

```powershell
python -m unittest discover -s tests -v
```

All four local unit tests passed:
1. A/C instruction encoding and label resolution.
2. Duplicate-label warning.
3. Invalid computation rejection.
4. Variable allocation.

`Box.asm` assembled successfully into 51 instructions. The generated output matched the existing `Box.hack` exactly.

## Official Verification Pending

The official Hardware Simulator tests and CPU Emulator visual test have not yet been executed. The official `.tst` and `.cmp` files were not included in the supplied capstone materials. Obtain the official test scripts and reference assembler from the course repository before final verification.

Local Python tests do not replace official HDL simulator tests. Do not claim official tests have passed until they are actually run.

## Assembler Features

- Two-pass assembly and label resolution.
- Predefined Hack symbols: `SP`, `LCL`, `ARG`, `THIS`, `THAT`, `R0`–`R15`, `SCREEN` and `KBD`.
- Variable allocation beginning at RAM address 16.
- A-instruction and C-instruction encoding.
- Invalid instruction handling.
- Duplicate-label warning for `K mod 3 = 2`; the first definition is retained.

## Submission Checklist

- [ ] Run official CPU, Memory and Computer HDL tests.
- [ ] Compare Add, Max, Rect and Pong with the official assembler.
- [ ] Verify duplicate-label warning behaviour.
- [ ] Run `Box.hack` in the CPU Emulator.
- [ ] Capture genuine test evidence.
- [ ] Update the report with actual verification results.
- [ ] Include only required capstone files in the final submission.
