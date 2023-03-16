#!/usr/bin/env Rscript
# script to compile report from pipeline data
library("argparse")

VERSION="0.2.1"


# start arg parser
parser <- ArgumentParser()
parser$add_argument("--output_dir", help="Output directory") # ToDo: make default current working dir. default=default_output_dir, 
parser$add_argument("--argosDir", help="argosDir Project path")
# parser$add_argument("--geneAnnotation_path", help="Gene annotation file")
parser$add_argument("--sampleID", help="Sample id")
parser$add_argument("-o", "--output_file", default="report999.html", help="Output filename")

args <- parser$parse_args()

params = list(
        argosDir = args$argosDir,
        ##geneAnnotation_path = args$geneAnnotation_path,
        sampleID=args$sampleID
    )




# compile the HTML report
rmarkdown::render(
    input = "report_sample_level.Rmd", 
    params = params,
    output_format = "html_document",
    output_file = args$output_file,
    output_dir = args$output_dir,
    # intermediates_dir = args$intermediates_dir, 
    clean = TRUE
)

