#!/usr/bin/env Rscript
# script to compile report from pipeline data
library("argparse")


# compile the HTML report
rmarkdown::render(
    "report_sample_level.Rmd"
)
