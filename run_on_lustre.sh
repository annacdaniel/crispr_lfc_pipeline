#!/bin/bash/

bsub \
-q normal \
-o ./tests/log.txt \
-e ./tests/err.txt \
-R"select[mem>4000] rusage[mem=4000]" \
-M 4000 \
"module load nextflow-23.10.0 ISG/singularity \
&& nextflow run main.nf -c nextflow.config -profile lsf_ibar"