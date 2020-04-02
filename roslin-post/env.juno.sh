#!/bin/bash
# top-level environment needed to run Nextflow on Juno HPC
module unload java && module load java/jdk1.8.0_202
module unload singularity && module load singularity/3.1.1
