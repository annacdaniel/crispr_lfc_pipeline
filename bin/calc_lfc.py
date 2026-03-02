#!/usr/bin/env python3
"""
calc_lfc.py
Calculate log2 fold change for each key in the cell file relative to the
plasmid. Pseudocount of 1 is added to raw normalised values before taking log.
Keys with no matching entry in the plasmid file are dropped (with a warning).

LFC = log2((cell_norm + pseudocount) / (plasmid_norm + pseudocount))

Input:  normalised cell counts TSV    (key, norm_count)
        normalised plasmid counts TSV (key, norm_count)
Output: LFC TSV (key, cell_norm, plasmid_norm, lfc)
"""

import argparse
import csv
import math
import sys


PSEUDOCOUNT = 1e-8   # added to normalised frequencies before log


def parse_args():
    p = argparse.ArgumentParser(description="Calculate log2 fold change")
    p.add_argument("--cell",    required=True, help="Normalised cell counts TSV")
    p.add_argument("--plasmid", required=True, help="Normalised plasmid counts TSV")
    p.add_argument("--output",  required=True, help="Output LFC TSV")
    p.add_argument(
        "--pseudocount",
        type=float,
        default=PSEUDOCOUNT,
        help=f"Pseudocount added to normalised values before log (default: {PSEUDOCOUNT})",
    )
    return p.parse_args()


def load_counts(path):
    """Return dict: key -> float(norm_count)."""
    counts = {}
    with open(path) as fh:
        reader = csv.reader(fh, delimiter="\t")
        for line_no, row in enumerate(reader, start=1):
            if len(row) != 2:
                print(f"WARNING: skipping malformed line {line_no} in {path}", file=sys.stderr)
                continue
            key, value = row
            try:
                counts[key] = float(value)
            except ValueError:
                print(f"WARNING: non-numeric value on line {line_no}: {value!r}", file=sys.stderr)
    return counts


def main():
    args = parse_args()

    cell_counts    = load_counts(args.cell)
    plasmid_counts = load_counts(args.plasmid)

    print(f"Cell keys:    {len(cell_counts)}", file=sys.stderr)
    print(f"Plasmid keys: {len(plasmid_counts)}", file=sys.stderr)

    written = 0
    dropped = 0

    with open(args.output, "w") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["key", "cell_norm", "plasmid_norm", "lfc"])

        for key, cell_norm in cell_counts.items():
            if key not in plasmid_counts:
                dropped += 1
                continue

            plasmid_norm = plasmid_counts[key]
            lfc = math.log2(
                (cell_norm    + args.pseudocount) /
                (plasmid_norm + args.pseudocount)
            )
            writer.writerow([key, cell_norm, plasmid_norm, lfc])
            written += 1

    print(f"Written {written} LFC rows; dropped {dropped} unmatched keys", file=sys.stderr)


if __name__ == "__main__":
    main()
