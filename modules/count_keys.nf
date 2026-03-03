process COUNT_KEYS {
    tag "count_keys"

    input:
    path mapped_counts

    output:
    path "key_counts.txt", emit: counts_table

    script:
    """
    count_keys.py \\
        --input  ${mapped_counts} \\
        --output key_counts.txt
    """
}
