process BIN_BY_GENE {
    tag "bin_by_gene"

    input:
    path mapped_counts

    output:
    path "bin_*.txt", emit: bins

    script:
    """
    bin_by_gene.py \\
        --input   ${mapped_counts} \\
        --outdir  .
    """
}
