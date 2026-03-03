#!/bin/bash/
#BSUB -o ./tests/log.txt
#BSUB -e ./tests/err.txt
#BSUB -q normal
#BSUB -n 2
#BSUB -R"select[mem>4000] rusage[mem=4000]" 
#BSUB -M 4000

# export NXF_ANSI_LOG=false
# # export NXF_OPTS="-Xms8G -Xmx8G -Dnxf.pool.maxThreads=2000"
# # export NXF_VER=22.04.0-5697

# module load nextflow-23.10.0 ISG/singularity

# nextflow run \
# main.nf \
# -c nextflow.config

# bsub -q normal -o .o -e n.e -R"span[hosts=1]" -R"select[mem>4000] rusage[mem=4000]" -M 4000 \
# "export JAVA_HOME='/software/jre1.8.0_201/'; export JAVA_CMD='/software/jre1.8.0_201/bin/java'; \
# export JAVA_TOOL_OPTIONS="-Xmx128M"; /lustre/scratch118/admin/team94/ac55/nextflow run /lustre/scratch118/admin/team94/ac55/index.nf"

# For reference: https://ssg-confluence.internal.sanger.ac.uk/spaces/FARM/pages/210700810/Nextflow+Best+Practices

bsub -q normal -o ./tests/log.txt -e ./tests/err.txt -R"select[mem>4000] rusage[mem=4000]" -M 4000 "module load nextflow-23.10.0 ISG/singularity && nextflow run main.nf -c nextflow.config"