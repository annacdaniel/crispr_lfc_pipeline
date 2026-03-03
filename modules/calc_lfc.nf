process CALC_LFC {
    tag "calc_lfc"

    input:
    path mapped_counts
    path norm_plasmid

    output:
    path "lfc.txt", emit: lfc

    script:
    """
    calc_lfc.py \\
        --mapped  ${mapped_counts} \\
        --plasmid ${norm_plasmid} \\
        --output  lfc.txt
    """
}
