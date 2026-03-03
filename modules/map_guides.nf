process MAP_GUIDES {
    tag "map_guides"

    input:
    path norm_cell_counts
    path annotations

    output:
    path "mapped_counts.txt", emit: mapped

    script:
    """
    map_guides.py \\
        --counts      ${norm_cell_counts} \\
        --annotations ${annotations} \\
        --output      mapped_counts.txt
    """
}
