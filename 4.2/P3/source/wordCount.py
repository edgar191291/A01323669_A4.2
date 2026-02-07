# pylint: disable=invalid-name
"""
wordCount.py

Reads a text file and counts distinct words and their frequencies.
Words are separated by whitespace (spaces, tabs, new lines).

Normalization (beginner-friendly):
- lowercases text
- removes common punctuation from the start/end of tokens

Invalid/empty input is handled without stopping execution.
Results are printed and saved to WordCountResults.txt.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple


RESULTS_FILENAME = "WordCountResults.txt"


def normalize_word(token: str) -> str:
    """Normalize a token: lowercase and strip common punctuation."""
    return token.strip(".,;:!?\"'()[]{}").lower()


def read_words(file_path: Path) -> Tuple[List[str], List[str]]:
    """Read file and return (words, messages)."""
    messages: List[str] = []
    words: List[str] = []

    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        messages.append("File encoding error: could not read as UTF-8.")
        return words, messages

    tokens = text.split()
    if not tokens:
        messages.append("Warning: file contained no readable tokens.")
        return words, messages

    for token in tokens:
        word = normalize_word(token)
        if word:
            words.append(word)

    return words, messages


def count_frequencies(words: List[str]) -> Dict[str, int]:
    """Count word frequencies using a basic dictionary approach."""
    freq: Dict[str, int] = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


def build_report(freq: Dict[str, int], messages: List[str], elapsed_seconds: float) -> str:
    """Create output report string."""
    lines: List[str] = []
    lines.append("WORD COUNT RESULTS")
    lines.append("------------------")
    lines.append(f"DISTINCT WORDS: {len(freq)}")
    lines.append("")

    for word in sorted(freq.keys()):
        lines.append(f"{word}: {freq[word]}")

    lines.append("")

    if messages:
        lines.append("Messages while reading the file (execution continued):")
        lines.extend(messages)
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
        print("Usage: python wordCount.py fileWithData.txt")
        return 1

    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"Error: file not found -> {input_file}")
        return 1

    start = time.perf_counter()

    words, messages = read_words(input_file)
    freq = count_frequencies(words)

    elapsed = time.perf_counter() - start
    report = build_report(freq, messages, elapsed)

    print(report)

    out_path = write_results(Path.cwd(), report)
    print(f"\nResults file created: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
