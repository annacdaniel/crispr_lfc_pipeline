#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

include { NORMALISE       } from './modules/normalise'
include { MAP_GUIDES as MAP_GUIDES_CELL    } from './modules/map_guides'
include { MAP_GUIDES as MAP_GUIDES_PLASMID } from './modules/map_guides'
include { BIN_BY_GENE     } from './modules/bin_by_gene'
include { COUNT_KEYS as COUNT_KEYS_CELL    } from './modules/count_keys'
include { COUNT_KEYS as COUNT_KEYS_PLASMID } from './modules/count_keys'
include { CALC_LFC        } from './modules/calc_lfc'

workflow {

    // ── Inputs ────────────────────────────────────────────────────────────────
    ch_cell_counts    = Channel.fromPath(params.cell_counts,    checkIfExists: true)
    ch_plasmid_counts = Channel.fromPath(params.plasmid_counts, checkIfExists: true)
    ch_annotations    = Channel.fromPath(params.annotations,    checkIfExists: true)

    // ── Step 1: Normalise both count files ────────────────────────────────────
    NORMALISE(
        ch_cell_counts.map    { f -> tuple("cell",    f) }
            .mix(
        ch_plasmid_counts.map { f -> tuple("plasmid", f) })
    )

    ch_norm_cell    = NORMALISE.out.normalised.filter { label, f -> label == "cell"    }
    ch_norm_plasmid = NORMALISE.out.normalised.filter { label, f -> label == "plasmid" }

    // ── Step 2: Map keys → guide pair → gene pair for both count sets ─────────
    MAP_GUIDES_CELL(
        ch_norm_cell.map { _label, f -> f },
        ch_annotations
    )

    MAP_GUIDES_PLASMID(
        ch_norm_plasmid.map { _label, f -> f },
        ch_annotations
    )

    // ── Step 3: Count unique keys per guide pair / gene pair ──────────────────
    COUNT_KEYS_CELL(MAP_GUIDES_CELL.out.mapped)
    COUNT_KEYS_PLASMID(MAP_GUIDES_PLASMID.out.mapped)

    // ── Step 4: Calculate LFC and emit enriched table ─────────────────────────
    //   Use mapped cell rows + normalised plasmid counts to compute per-key LFC
    ch_norm_plasmid_file = ch_norm_plasmid.map { _l, f -> f }

    CALC_LFC(
        MAP_GUIDES_CELL.out.mapped,
        ch_norm_plasmid_file
    )

    // ── Step 5: Bin LFC table by gene pair (for parallel downstream) ──────────
    BIN_BY_GENE(CALC_LFC.out.lfc)

    // Each element of ch_bins is: tuple(gene_pair_label, binned_file)
    ch_bins = BIN_BY_GENE.out.bins.flatten().map { f ->
        def label = f.baseName.replaceAll(/^bin_/, '')
        tuple(label, f)
    }
}
