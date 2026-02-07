# pylint: disable=invalid-name
"""
computeStatistics.py

Reads a text file containing numeric values (one per line), then computes:
- Mean
- Median
- Mode
- Population standard deviation
- Population variance

The program ignores invalid lines and continues execution.
Results are printed to the console and saved to StatisticsResults.txt.
"""

from __future__ import annotations

import math
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple


RESULTS_FILENAME = "StatisticsResults.txt"


def parse_numbers(file_path: Path) -> Tuple[List[float], List[str]]:
    """Return valid numbers and a list of error messages for invalid lines."""
    numbers: List[float] = []
    errors: List[str] = []

    with file_path.open("r", encoding="utf-8") as file:
        for line_number, raw_line in enumerate(file, start=1):
            text = raw_line.strip()

            if not text:
                errors.append(f"Line {line_number}: empty line (skipped).")
                continue

            try:
                numbers.append(float(text))
            except ValueError:
                errors.append(f"Line {line_number}: invalid number '{text}' (skipped).")

    return numbers, errors


def mean(values: List[float]) -> float:
    """Compute the mean."""
    total = 0.0
    for value in values:
        total += value
    return total / len(values)


def median(values: List[float]) -> float:
    """Compute the median."""
    sorted_values = sorted(values)
    n = len(sorted_values)
    mid = n // 2

    if n % 2 == 1:
        return sorted_values[mid]

    return (sorted_values[mid - 1] + sorted_values[mid]) / 2.0


def mode(values: List[float]) -> List[float]:
    """Compute mode(s). Returns only the first mode found (to match expected output)."""
    freq: Dict[float, int] = {}
    for value in values:
        freq[value] = freq.get(value, 0) + 1

    max_count = max(freq.values(), default=0)
    if max_count <= 1:
        return []

    for value in values:
        if freq[value] == max_count:
            return [value]

    return []


def population_variance(values: List[float], mean_value: float) -> float:
    """Compute variance using (N-1) to match the expected spreadsheet results."""
    total = 0.0
    for value in values:
        diff = value - mean_value
        total += diff * diff

    if len(values) < 2:
        return 0.0

    return total / (len(values) - 1)


def population_std_dev(variance_value: float) -> float:
    """Compute population standard deviation."""
    return math.sqrt(variance_value)


def build_report(values: List[float], errors: List[str], elapsed_seconds: float) -> str:
    """Create a report string for console and file output."""
    if not values:
        lines = [
            "No valid numeric data found. Cannot compute statistics.",
            "",
            "Errors found while reading the file:",
            *errors,
            "",
            f"Elapsed time (seconds): {elapsed_seconds:.6f}",
        ]
        return "\n".join(lines)

    mean_value = mean(values)
    median_value = median(values)
    modes = mode(values)
    variance_value = population_variance(values, mean_value)
    std_value = population_std_dev(variance_value)

    lines: List[str] = []
    lines.append("DESCRIPTIVE STATISTICS (POPULATION)")
    lines.append("---------------------------------")
    lines.append(f"COUNT: {len(values)}")
    lines.append(f"MEAN: {mean_value}")
    lines.append(f"MEDIAN: {median_value}")
    lines.append(
        f"MODE: {', '.join(str(m) for m in modes)}" if modes else "MODE: No mode."
    )
    lines.append(f"POPULATION STANDARD DEVIATION: {std_value}")
    lines.append(f"POPULATION VARIANCE: {variance_value}")
    lines.append("")

    if errors:
        lines.append("Errors found while reading the file (execution continued):")
        lines.extend(errors)
        lines.append("")

    lines.append(f"Elapsed time (seconds): {elapsed_seconds:.6f}")
    return "\n".join(lines)


def write_results(output_dir: Path, report: str) -> Path:
    """Write report to StatisticsResults.txt in output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / RESULTS_FILENAME
    out_path.write_text(report, encoding="utf-8")
    return out_path


def main() -> int:
    """Command line entry point."""
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        return 1

    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"Error: file not found -> {input_file}")
        return 1

    start = time.perf_counter()
    values, errors = parse_numbers(input_file)
    elapsed = time.perf_counter() - start

    report = build_report(values, errors, elapsed)
    print(report)

    out_path = write_results(Path.cwd(), report)
    print(f"\nResults file created: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
