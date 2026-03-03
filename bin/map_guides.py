#!/usr/bin/env python3
"""
map_guides.py
Parse keys of the form {guide1_ID}_{iBAR}_{guide2_ID}, look up gene targets
for each guide ID from the annotations file, and output an enriched TSV.

Input counts format:  key<TAB>normalised_count
Annotations format:   guide_sequence<TAB>guide_id<TAB>gene (no header, guide_sequence unused)

Output columns: key, ibar, guide1_id, guide2_id, gene1, gene2, norm_count
"""

import argparse
import csv
import sys


def parse_args():
    p = argparse.ArgumentParser(description="Map keys to guide and gene pairs")
    p.add_argument("--counts",      required=True, help="Normalised counts TSV")
    p.add_argument("--annotations", required=True, help="Guide ID → gene TSV")
    p.add_argument("--output",      required=True, help="Output mapped counts TSV")
    return p.parse_args()


def load_annotations(path):
    """Return dict: guide_id (str) -> gene (str).
    
    Expected format: guide_sequence<TAB>guide_id<TAB>gene
    """
    ann = {}
    with open(path) as fh:
        reader = csv.reader(fh, delimiter="\t")
        for row in reader:
            if len(row) < 3:
                continue
            guide_sequence, guide_id, gene = row[0].strip(), row[1].strip(), row[2].strip()
            ann[guide_id] = gene
    return ann


def parse_key(key):
    """
    Split key into (guide1_id, ibar, guide2_id).
    Key format: {guide1_ID}_{iBAR}_{guide2_ID}
    The iBAR is always the middle token (index 1).
    guide IDs themselves never contain '_'.
    """
    parts = key.split("_")
    if len(parts) != 3:
        raise ValueError(f"Key does not have exactly 3 '_'-delimited parts: {key!r}")
    guide1_id, ibar, guide2_id = parts
    return guide1_id, ibar, guide2_id


def main():
    args = parse_args()

    ann = load_annotations(args.annotations)
    print(f"Loaded {len(ann)} guide→gene mappings", file=sys.stderr)

    written = 0
    skipped = 0

    with open(args.counts) as in_fh, open(args.output, "w") as out_fh:
        reader = csv.reader(in_fh, delimiter="\t")
        writer = csv.writer(out_fh, delimiter="\t")
        writer.writerow(["key", "ibar", "guide1_id", "guide2_id", "gene1", "gene2", "norm_count"])

        for line_no, row in enumerate(reader, start=1):
            if len(row) != 2:
                print(f"WARNING: skipping malformed line {line_no}: {row}", file=sys.stderr)
                skipped += 1
                continue

            key, norm_count = row

            try:
                guide1_id, ibar, guide2_id = parse_key(key)
            except ValueError as e:
                print(f"WARNING: {e}", file=sys.stderr)
                skipped += 1
                continue

            if guide1_id not in ann:
                print(f"WARNING: guide1_id {guide1_id!r} not found in annotations (line {line_no})", file=sys.stderr)
                skipped += 1
                continue

            if guide2_id not in ann:
                print(f"WARNING: guide2_id {guide2_id!r} not found in annotations (line {line_no})", file=sys.stderr)
                skipped += 1
                continue

            gene1 = ann[guide1_id]
            gene2 = ann[guide2_id]

            writer.writerow([key, ibar, guide1_id, guide2_id, gene1, gene2, norm_count])
            written += 1

    print(f"Written {written} mapped rows; skipped {skipped}", file=sys.stderr)


if __name__ == "__main__":
    main()