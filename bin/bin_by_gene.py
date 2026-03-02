#!/usr/bin/env python3
"""
bin_by_gene.py
Split a mapped counts file into one file per gene pair for parallel downstream
processing. Output files are named bin_<gene1>~<gene2>.txt

Input: mapped counts TSV (output of map_guides.py)
Output: one TSV per gene pair written to --outdir
"""

import argparse
import csv
import os
import sys
from collections import defaultdict


def parse_args():
    p = argparse.ArgumentParser(description="Bin mapped counts by gene pair")
    p.add_argument("--input",  required=True, help="Mapped counts TSV")
    p.add_argument("--outdir", required=True, help="Directory for output bin files")
    return p.parse_args()


def safe_filename(gene_pair_label):
    """Replace characters unsafe for filenames."""
    return gene_pair_label.replace("/", "_").replace(" ", "_")


def main():
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    bins = defaultdict(list)
    header = None

    with open(args.input) as fh:
        reader = csv.reader(fh, delimiter="\t")
        header = next(reader)  # consume header row

        gene1_idx = header.index("gene1")
        gene2_idx = header.index("gene2")

        for row in reader:
            gene1 = row[gene1_idx]
            gene2 = row[gene2_idx]
            gene_pair = f"{gene1}~{gene2}"
            bins[gene_pair].append(row)

    writers = {}
    file_handles = {}

    try:
        for gene_pair, rows in bins.items():
            fname = os.path.join(args.outdir, f"bin_{safe_filename(gene_pair)}.txt")
            fh = open(fname, "w")
            file_handles[gene_pair] = fh
            w = csv.writer(fh, delimiter="\t")
            w.writerow(header)
            for row in rows:
                w.writerow(row)
    finally:
        for fh in file_handles.values():
            fh.close()

    print(f"Created {len(bins)} gene-pair bin files in {args.outdir}", file=sys.stderr)


if __name__ == "__main__":
    main()
