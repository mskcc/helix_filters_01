#!/usr/bin/env Rscript
# script to compile report from pipeline data
library("argparse")

# need to get the path to this script
args <- commandArgs(trailingOnly = F)  
scriptPath <- normalizePath(dirname(sub("^--file=", "", args[grep("^--file=", args)])))

# need to set some default locations
# NOTE: rmarkdown::render by default tries to write all intermediaries and outputs
# to the same dir as the input Rmd file !! this can cause issues inside read-only Singularity container 
default_output_dir <- normalizePath(getwd())
default_output_file <- file.path(default_output_dir, "report.html")
default_Rdata <- file.path(default_output_dir, "report.Rdata")

# start arg parser
parser <- ArgumentParser()
parser$add_argument("-o", "--output_file", default=default_output_file, help="Output filename")
parser$add_argument("--output_dir", default=default_output_dir, help="Output filename")
parser$add_argument("--template", default=file.path(scriptPath, "main.Rmd"), help="R Markdown main report template file (.Rmd)")
parser$add_argument("--mutations", dest = 'mut_file', default="data_mutations_extended.txt", help="Mutations file")
parser$add_argument("--samples", dest = 'sample_file', default="data_clinical_sample.txt", help="Samples file")
parser$add_argument("--patients", dest = 'patient_file', default="data_clinical_patient.txt", help="Patients file")
parser$add_argument("--intermediates", dest = 'intermediates_dir', default=default_output_dir, help="Location for intermediates to be written to")
parser$add_argument("--Rdata", dest = 'Rdata_file', default=default_Rdata, help="Rdata file to save for report")

args <- parser$parse_args()

# compile the HTML report
rmarkdown::render(
    input = args$template, 
    params = list(
        mut_file = args$mut_file,
        sample_file = args$sample_file,
        patient_file = args$patient_file,
        Rdata_file = args$Rdata_file
    ),
    output_format = "html_document",
    output_file = args$output_file,
    output_dir = args$output_dir,
    intermediates_dir = args$intermediates_dir, 
    clean = TRUE
)
