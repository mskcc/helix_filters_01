#!/usr/bin/env Rscript

# Script to do a full outer join merge of multiple tables
# Designed to accept one Table 1 (t1) and 0 or more Table 2's (t2)
# If only t1 is provided, it gets parsed and saved as output
# If t2's are provided, all tables get merged together
# NOTE: tables should all have unique column labels except for the common join column key label

# $ module load R/R-3.6.1
library("argparse")
parser <- ArgumentParser()
parser$add_argument("-2", "--t2", default=NULL, help="One or more tables to merge against Table 1", nargs = "+")
parser$add_argument("-o", "--output_file", default="out.tsv", help="Output filename")
parser$add_argument("-k", "--key", default=NULL, help="Merge column key", required = TRUE)
parser$add_argument("--include-cols-file", default=NULL, dest = "include_cols_file", 
                    help="File with list of columns to include in the output")
parser$add_argument("t1", nargs=1, help="Table 1 file to be used for merge")
args <- parser$parse_args()

t1_filename <- args$t1
t2_filenames <- args$t2
output_filename <- args$output_file
join_colname <- args$key # join_colname <- c('Hugo_Symbol')
include_cols_file <- args$include_cols_file

# helper function to subset some columsn in the multi-table merge output
subset_cols <- function(df, keep_cols){
    old_cols <- colnames(df)
    final_cols <- old_cols[old_cols %in% keep_cols]
    df <- df[, final_cols, drop = FALSE]
    return(df)
}

# load optional output column whitelist
include_cols <- NULL
if(!is.null(include_cols_file)){
    include_cols <- readLines(include_cols_file)
}
# save.image()


# check if a t2 table was passed; if so, do the merge, if not, copy the t1 to output filename
# do it like this to make conditional execution in the pipeline easier
single_file_mode <- is.null(t2_filenames)

if(single_file_mode){
    # parse table 1 and save it as output
    # NOTE: do not just copy the file because we need to have the R data frame handling for NA values, etc.
    t1 <- read.delim(file =t1_filename, 
                     header = TRUE, 
                     sep = '\t', 
                     na.strings = c('', '.', 'NA'), 
                     check.names = FALSE)
    write.table(x = t1, file = output_filename, quote = FALSE, sep = '\t', row.names = FALSE, col.names = TRUE)

    } else {
    # merge 2 or more tables together
    
    # make list of all tables and their colnames
    col_names <- list()
    table_list <- list()
    
    # load t1
    table_list[["t1"]] <- read.delim(file =t1_filename, 
                                     header = TRUE, 
                                     sep = '\t', 
                                     na.strings = c('', '.', 'NA'), 
                                     check.names = FALSE)
    if(!is.null(include_cols)){
        table_list[["t1"]] <- subset_cols(df = table_list[["t1"]], c(join_colname, include_cols))
    }
    col_names[["t1"]] <- colnames(table_list[["t1"]])[! colnames(table_list[["t1"]]) %in% join_colname]
    
    # load all other tables
    for(i in seq(length(t2_filenames))){
        filename <- t2_filenames[[i]]
        label <- paste(c('t2_', i), collapse = '')
        table_list[[label]] <- read.delim(file = filename, 
                                          header = TRUE, 
                                          sep = '\t', 
                                          na.strings = c('', '.', 'NA'),
                                          check.names = FALSE)
        if(!is.null(include_cols)){
            table_list[[label]] <- subset_cols(df = table_list[[label]], c(join_colname, include_cols))
        }
        col_names[[label]] <- colnames(table_list[[label]])[! colnames(table_list[[label]]) %in% join_colname]
    }

    # NOTE: need to make sure there are no duplicate names or it will cause duplicate output entries
    all_cols <- Reduce(c, col_names)
    duplicated_cols <- duplicated(all_cols)
    if (any(duplicated_cols)){
        stop(paste(c("ERROR: input tables have non-unique columns; ", all_cols[duplicated_cols]), collapse = ' '))
    }
    
    # merge all tables
    # NOTE: WARNING! This operation can become very slow and/or resource intensive for large amounts of large tables!
    t3 <- Reduce(function(t1, t2) merge(t1, t2, by = join_colname, all = TRUE), table_list)
    write.table(x = t3, file = output_filename, quote = FALSE, sep = '\t', row.names = FALSE, col.names = TRUE)
}

