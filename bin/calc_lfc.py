#!/usr/bin/env python3
"""
calc_lfc.py
Calculate log2 fold change for each key in mapped cell counts relative to the
normalised plasmid counts. Keys with no matching entry in plasmid are dropped
(with a warning).

LFC = log2((cell_norm + pseudocount) / (plasmid_norm + pseudocount))

Input:  mapped counts TSV             (key, ibar, guide1_id, guide2_id, gene1, gene2, norm_count)
        normalised plasmid counts TSV (key, norm_count)
Output: LFC TSV (key, ibar, guide1_id, guide2_id, gene1, gene2, lfc)
"""

import argparse
import csv
import math
import sys


PSEUDOCOUNT = 1e-8   # added to normalised frequencies before log


def parse_args():
    p = argparse.ArgumentParser(description="Calculate log2 fold change")
    p.add_argument("--mapped",  required=True, help="Mapped cell counts TSV")
    p.add_argument("--plasmid", required=True, help="Normalised plasmid counts TSV")
    p.add_argument("--output",  required=True, help="Output LFC TSV")
    p.add_argument(
        "--pseudocount",
        type=float,
        default=PSEUDOCOUNT,
        help=f"Pseudocount added to normalised values before log (default: {PSEUDOCOUNT})",
    )
    return p.parse_args()


def load_plasmid_counts(path):
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


def load_mapped_rows(path):
    """Yield mapped rows with required fields and parsed norm_count."""
    required_cols = ["key", "ibar", "guide1_id", "guide2_id", "gene1", "gene2", "norm_count"]

    with open(path) as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        if reader.fieldnames is None:
            print(f"ERROR: mapped file {path} is empty or missing header", file=sys.stderr)
            sys.exit(1)

        missing = [c for c in required_cols if c not in reader.fieldnames]
        if missing:
            print(f"ERROR: mapped file missing required columns: {', '.join(missing)}", file=sys.stderr)
            sys.exit(1)

        for line_no, row in enumerate(reader, start=2):
            try:
                row["norm_count"] = float(row["norm_count"])
            except ValueError:
                print(
                    f"WARNING: non-numeric norm_count on line {line_no}: {row['norm_count']!r}",
                    file=sys.stderr,
                )
                continue
            yield row


def main():
    args = parse_args()

    plasmid_counts = load_plasmid_counts(args.plasmid)

    print(f"Plasmid keys: {len(plasmid_counts)}", file=sys.stderr)

    written = 0
    dropped = 0

    with open(args.output, "w") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["key", "ibar", "guide1_id", "guide2_id", "gene1", "gene2", "lfc"])

        for row in load_mapped_rows(args.mapped):
            key = row["key"]
            cell_norm = row["norm_count"]
            if key not in plasmid_counts:
                dropped += 1
                continue

            plasmid_norm = plasmid_counts[key]
            lfc = math.log2(
                (cell_norm    + args.pseudocount) /
                (plasmid_norm + args.pseudocount)
            )
            writer.writerow([
                key,
                row["ibar"],
                row["guide1_id"],
                row["guide2_id"],
                row["gene1"],
                row["gene2"],
                lfc,
            ])
            written += 1

    print(f"Written {written} LFC rows; dropped {dropped} unmatched keys", file=sys.stderr)


if __name__ == "__main__":
    main()
