process CALC_LFC {
    tag "calc_lfc"

    input:
    tuple path(norm_cell), path(norm_plasmid)

    output:
    path "lfc.txt", emit: lfc

    script:
    """
    calc_lfc.py \\
        --cell    ${norm_cell} \\
        --plasmid ${norm_plasmid} \\
        --output  lfc.txt
    """
}
