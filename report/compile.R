#!/usr/bin/env Rscript
# script to compile report from pipeline data
library("argparse")

# need to get the path to this script
args <- commandArgs(trailingOnly = F)  
scriptPath <- normalizePath(dirname(sub("^--file=", "", args[grep("^--file=", args)])))

# start arg parser
parser <- ArgumentParser()
parser$add_argument("-o", "--output_file", default="report.html", help="Output filename")
parser$add_argument("--template", default=file.path(scriptPath, "main.Rmd"), help="R Markdown main report template file (.Rmd)")
parser$add_argument("--mutations", dest = 'mut_file', default="data_mutations_extended.txt", help="Mutations file")
parser$add_argument("--samples", dest = 'sample_file', default="data_clinical_sample.txt", help="Samples file")
parser$add_argument("--patients", dest = 'patient_file', default="data_clinical_patient.txt", help="Patients file")
args <- parser$parse_args()

# compile the HTML report
rmarkdown::render(
    input = args$template, 
    params = list(
        mut_file = args$mut_file,
        sample_file = args$sample_file,
        patient_file = args$patient_file
    ),
    output_format = "html_document",
    output_file = args$output_file
)
