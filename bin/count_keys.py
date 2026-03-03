#!/usr/bin/env python3
"""
count_keys.py
For each (guide_pair, gene_pair), count the number of unique keys (iBARs).

Input:  mapped counts TSV (output of map_guides.py)
Output: table with columns: gene_pair, guide_pair, n_ibars
        gene_pair  format: gene1~gene2
        guide_pair format: guide1ID_guide2ID
"""

import argparse
import csv
import sys
from collections import defaultdict


def parse_args():
    p = argparse.ArgumentParser(description="Count unique keys per guide/gene pair")
    p.add_argument("--input",  required=True, help="Mapped counts TSV")
    p.add_argument("--output", required=True, help="Output counts table TSV")
    return p.parse_args()


def main():
    args = parse_args()

    # counts[(gene_pair, guide_pair)] -> set of keys
    key_sets = defaultdict(set)

    with open(args.input) as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            gene_pair  = f"{row['gene1']}~{row['gene2']}"
            guide_pair = f"{row['guide1_id']}_{row['guide2_id']}"
            key_sets[(gene_pair, guide_pair)].add(row["key"])

    with open(args.output, "w") as fh:
        writer = csv.writer(fh, delimiter="\t")
        writer.writerow(["gene_pair", "guide_pair", "n_ibars"])
        for (gene_pair, guide_pair), keys in sorted(key_sets.items()):
            writer.writerow([gene_pair, guide_pair, len(keys)])

    print(f"Wrote {len(key_sets)} guide-pair rows to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
