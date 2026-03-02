#!/usr/bin/env python3
"""
normalise.py
Normalise counts by dividing each count by the total count for that file.
Input format: key<TAB>count
"""

import argparse
import csv
import sys


def parse_args():
    p = argparse.ArgumentParser(description="Normalise raw counts")
    p.add_argument("--input",  required=True, help="Input counts file (TSV: key, count)")
    p.add_argument("--output", required=True, help="Output normalised counts file")
    return p.parse_args()


def main():
    args = parse_args()

    rows = []
    total = 0

    with open(args.input) as fh:
        reader = csv.reader(fh, delimiter="\t")
        for line_no, row in enumerate(reader, start=1):
            if len(row) != 2:
                print(f"WARNING: skipping malformed line {line_no}: {row}", file=sys.stderr)
                continue
            key, raw_count = row
            try:
                count = int(raw_count)
            except ValueError:
                print(f"WARNING: non-integer count on line {line_no}: {raw_count!r}", file=sys.stderr)
                continue
            rows.append((key, count))
            total += count

    if total == 0:
        print("ERROR: total count is 0 — cannot normalise.", file=sys.stderr)
        sys.exit(1)

    with open(args.output, "w") as fh:
        writer = csv.writer(fh, delimiter="\t")
        for key, count in rows:
            normalised = count / total
            writer.writerow([key, normalised])

    print(f"Normalised {len(rows)} keys (total count = {total})", file=sys.stderr)


if __name__ == "__main__":
    main()
