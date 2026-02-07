# pylint: disable=invalid-name
"""
convertNumbers.py

Reads a text file containing integers (one per line) and converts each valid
integer to:
- Binary representation (base 2)
- Hexadecimal representation (base 16)

The conversion uses basic repeated-division algorithms (no bin(), no hex()).
Invalid lines are reported but do not stop execution.
Results are printed and saved to ConvertionResults.txt.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import List, Tuple


RESULTS_FILENAME = "ConvertionResults.txt"
HEX_DIGITS = "0123456789ABCDEF"


def parse_integers(file_path: Path) -> Tuple[List[int], List[str]]:
    """Parse integers from the input file; return (values, errors)."""
    values: List[int] = []
    errors: List[str] = []

    with file_path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            text = raw_line.strip()

            if not text:
                errors.append(f"Line {line_number}: empty line (skipped).")
                continue

            try:
                values.append(int(text))
            except ValueError:
                errors.append(f"Line {line_number}: invalid integer '{text}' (skipped).")

    return values, errors


def to_base(number: int, base: int) -> str:
    """Convert an integer to base 2 or 16 using repeated division."""
    if number == 0:
        return "0"

    is_negative = number < 0
    n = -number if is_negative else number

    digits: List[str] = []
    while n > 0:
        remainder = n % base
        if base == 16:
            digits.append(HEX_DIGITS[remainder])
        else:
            digits.append(str(remainder))
        n //= base

    digits.reverse()
    result = "".join(digits)
    return f"-{result}" if is_negative else result


def build_report(values: List[int], errors: List[str], elapsed_seconds: float) -> str:
    """Create output report string."""
    lines: List[str] = []
    lines.append("NUMBER CONVERSION RESULTS")
    lines.append("-------------------------")
    lines.append("FORMAT: DECIMAL -> BINARY | HEX")
    lines.append("")

    for value in values:
        binary = to_base(value, 2)
        hexa = to_base(value, 16)
        lines.append(f"{value} -> {binary} | {hexa}")

    lines.append("")

    if errors:
        lines.append("Errors found while reading the file (execution continued):")
        lines.extend(errors)
        lines.append("")

    lines.append(f"Elapsed time (seconds): {elapsed_seconds:.6f}")
    return "\n".join(lines)


def write_results(output_dir: Path, report: str) -> Path:
    """Write report to results file in output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / RESULTS_FILENAME
    out_path.write_text(report, encoding="utf-8")
    return out_path


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        return 1

    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"Error: file not found -> {input_file}")
        return 1

    start = time.perf_counter()
    values, errors = parse_integers(input_file)
    elapsed = time.perf_counter() - start

    report = build_report(values, errors, elapsed)
    print(report)

    out_path = write_results(Path.cwd(), report)
    print(f"\nResults file created: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
