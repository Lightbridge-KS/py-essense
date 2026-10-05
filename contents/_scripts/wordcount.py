"""Word-count CLI tool."""

import argparse
from collections import Counter
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description="Show the most common words in text files.",
    )
    parser.add_argument("files", nargs="+", type=Path, help="input text files")
    parser.add_argument(
        "-n",
        "--top",
        type=int,
        default=10,
        help="number of words (default: %(default)s)",
    )
    parser.add_argument(
        "-i", "--ignore-case", action="store_true", help="case-insensitive counting"
    )
    return parser


def count_words(files: list[Path], ignore_case: bool) -> Counter[str]:
    """Count words across all files."""
    counter: Counter[str] = Counter()
    for path in files:
        text: str = path.read_text(encoding="utf-8")
        counter.update((text.lower() if ignore_case else text).split())
    return counter


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return an exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)  # argv=None → uses sys.argv[1:]

    missing = [p for p in args.files if not p.is_file()]
    if missing:
        parser.error(f"file not found: {missing[0]}")  # usage + message, exit 2

    for word, n in count_words(args.files, args.ignore_case).most_common(args.top):
        print(f"{n:>6}  {word}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
