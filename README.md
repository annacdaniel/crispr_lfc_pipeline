# CRISPR LFC Pipeline

A Nextflow pipeline for calculating log fold change (LFC) from dual-guide CRISPR screen counts data.

## Pipeline Overview

```
cell_counts.txt ──┐
                  ├──[NORMALISE]──[MAP_GUIDES]──[BIN_BY_GENE]  → per-gene-pair bin files
plasmid_counts ──┘         │                └──[COUNT_KEYS]    → key_counts.txt
                           └──────────────────[CALC_LFC]       → lfc.txt
```

| Step | Process | Script | Output |
|------|---------|--------|--------|
| 1 | `NORMALISE` | `normalise.py` | `cell_normalised.txt`, `plasmid_normalised.txt` |
| 2 | `MAP_GUIDES` | `map_guides.py` | `mapped_counts.txt` |
| 3 | `BIN_BY_GENE` | `bin_by_gene.py` | `bin_<gene1>~<gene2>.txt` (one per gene pair) |
| 4 | `COUNT_KEYS` | `count_keys.py` | `key_counts.txt` |
| 5 | `CALC_LFC` | `calc_lfc.py` | `lfc.txt` |

## Input File Formats

### Count files (`--cell_counts`, `--plasmid_counts`)
Tab-separated, no header:
```
key<TAB>count
3258_CTCCCCCCGGCC_3258<TAB>10
```
Key format: `{guide1_ID}_{iBAR_sequence}_{guide2_ID}`

### Guide annotations (`--annotations`)
Tab-separated, optional header (`guide_id`, `gene`):
```
guide_id<TAB>gene
3258<TAB>BRCA1
```

## Usage

```bash
# Default (uses data/ directory)
nextflow run main.nf

# Custom inputs
nextflow run main.nf \
    --cell_counts    /path/to/cell_counts.txt \
    --plasmid_counts /path/to/plasmid_counts.txt \
    --annotations    /path/to/guide_annotations.txt \
    --outdir         results/

# With conda
nextflow run main.nf -profile conda

# On SLURM
nextflow run main.nf -profile slurm
```

## Output Files

| File | Description |
|------|-------------|
| `results/normalise/cell_normalised.txt` | Cell counts divided by total |
| `results/normalise/plasmid_normalised.txt` | Plasmid counts divided by total |
| `results/map_guides/mapped_counts.txt` | Keys enriched with guide/gene annotations |
| `results/bin_by_gene/bin_<gene_pair>.txt` | Per-gene-pair count files for parallel analysis |
| `results/count_keys/key_counts.txt` | Table of `gene_pair`, `guide_pair`, `n_ibars` |
| `results/calc_lfc/lfc.txt` | `key`, `cell_norm`, `plasmid_norm`, `lfc` |

### LFC formula
```
LFC = log2((cell_norm + pseudocount) / (plasmid_norm + pseudocount))
```
Default pseudocount: `1e-8`. Keys present in cell but absent in plasmid are dropped.

## Quick Test

```bash
nextflow run main.nf \
    --cell_counts    tests/data/cell_counts.txt \
    --plasmid_counts tests/data/plasmid_counts.txt \
    --annotations    tests/data/guide_annotations.txt \
    --outdir         test_results/
```

## Requirements

- Nextflow ≥ 23.04
- Python ≥ 3.8 (stdlib only — no extra packages required)
