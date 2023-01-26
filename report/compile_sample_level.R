#!/usr/bin/env Rscript
# script to compile report from pipeline data
library("argparse")


# need to get the path to this script
args <- commandArgs(trailingOnly = F)  

# start arg parser
parser <- ArgumentParser()
parser$add_argument("--project_path", help="Output filename")
parser$add_argument("--geneAnnotation_path", help="Output filename")

# compile the HTML report
# rmarkdown::render(
#     "report_sample_level.Rmd"
# )

args <- parser$parse_args()

# compile the HTML report
rmarkdown::render(
    input = "report_sample_level.Rmd", 
    params = list(
        project_path = args$project_path,
        geneAnnotation_path = args$geneAnnotation_path
    ),
    output_format = "html_document",
)
