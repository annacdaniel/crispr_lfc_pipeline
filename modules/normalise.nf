process NORMALISE {
    tag "${label}"

    input:
    tuple val(label), path(counts_file)

    output:
    tuple val(label), path("${label}_normalised.txt"), emit: normalised

    script:
    """
    normalise.py \\
        --input  ${counts_file} \\
        --output ${label}_normalised.txt
    """
}
