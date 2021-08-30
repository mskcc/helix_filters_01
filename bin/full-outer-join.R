#!/usr/bin/env Rscript
# $ module load R/R-3.6.1
# $ ./full-outer-join.R 1.tsv 2.tsv Hugo_Symbol o.tsv
library("argparse")
parser <- ArgumentParser()
parser$add_argument("-2", "--t2", default=NULL, help="Table 2 to merge against")
parser$add_argument("-o", "--output_file", default="out.tsv", help="Output filename")
parser$add_argument("-k", "--key", default=NULL, help="Merge column key", required = TRUE)
parser$add_argument("t1", nargs=1, help="Table 1 file to be used for merge")
args <- parser$parse_args()

t1_filename <- args$t1
t2_filename <- args$t2
output_filename <- args$output_file
join_colname <- args$key # join_colname <- c('Hugo_Symbol')

# check if a t2 table was passed; if so, do the merge, if not, copy the t1 to output filename
# do it like this because the pipelines cannot handle optional file inputs, etc.
single_file_mode <- is.null(t2_filename)

if(single_file_mode){
    print(c("copying file", output_filename))
    # NOTE: do not just copy the file because we need to have the R data frame handling for NA values, etc.
    # res <- file.copy(t1_filename, output_filename, overwrite = TRUE)
    t1 <- read.delim(file =t1_filename, header = TRUE, sep = '\t', na.strings = c('', '.', 'NA'))
    write.table(x = t1, file = output_filename, quote = FALSE, sep = '\t', row.names = FALSE, col.names = TRUE)
} else {
    print("merging")
    t1 <- read.delim(file =t1_filename, header = TRUE, sep = '\t', na.strings = c('', '.', 'NA'))
    t2 <- read.delim(file = t2_filename, header = TRUE, sep = '\t', na.strings = c('', '.', 'NA'))
    
    # NOTE: need to make sure there are no duplicate names or it will cause duplicate output entries
    t1_cols <- colnames(t1)[! colnames(t1) %in% join_colname]
    t2_cols <- colnames(t2)[! colnames(t2) %in% join_colname]
    common_cols <- intersect(t1_cols, t2_cols)
    if (length(common_cols) > 0){
        stop(paste(c("ERROR: input tables have common columns; ", common_cols), collapse = ' '))
    }
    
    # merge the two tables
    t3 <- merge(x = t1, y = t2, by = join_colname, all = TRUE)
    write.table(x = t3, file = output_filename, quote = FALSE, sep = '\t', row.names = FALSE, col.names = TRUE)
}

