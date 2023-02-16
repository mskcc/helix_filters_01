#!/usr/bin/env Rscript
# script to compile report from pipeline data
library("argparse")

# need to get the path to this script
args <- commandArgs(trailingOnly = F)  
scriptPath <- normalizePath(dirname(sub("^--file=", "", args[grep("^--file=", args)])))


# need to set some default locations
# NOTE: rmarkdown::render by default tries to write all intermediaries and outputs
# to the same dir as the input Rmd file !! this can cause issues inside read-only Singularity container 
# default_output_dir <- normalizePath(getwd())
# default_output_file <- file.path(default_output_dir, "report.html")
# default_Rdata <- file.path(default_output_dir, "report.Rdata")



# start arg parser
parser <- ArgumentParser()
parser$add_argument("-o", "--output_file", default="report.html", help="Output filename")
parser$add_argument("--output_dir", help="Output directory") # ToDo: make default current working dir. default=default_output_dir, 
parser$add_argument("--project_path", help="Project path")
parser$add_argument("--geneAnnotation_path", help="Gene annotation file")
parser$add_argument("--sample_id", help="Sample id")
args <- parser$parse_args()

# compile the HTML report
rmarkdown::render(
    input = "/juno/work/ci/vurals/mutation_report/helix_filters_01/report/report_sample_level.Rmd", 
    params = list(
        project_path = args$project_path,
        geneAnnotation_path = args$geneAnnotation_path,
        sample_id=args$sample_id
    ),
    # output_format = "html_document",
    output_file = args$output_file,
    output_dir = args$output_dir,
    # intermediates_dir = args$intermediates_dir, 
    clean = TRUE
)


#Singularity mskcc_helix_filters_01-1.1:reporting.sif:/juno/work/ci/vurals/mutation_report> \
# Rscript helix_filters_01/report/compile_sample_level.R \
# --project_path /my_data/argos/11704_Y/1.1.2/20221102_20_40_060423/ 
# --geneAnnotation_path /my_data/geneAnnotation.rds 
