#!/usr/bin/env Rscript
# $ module load R/R-3.6.1
# $ ./full-outer-join.R 1.tsv 2.tsv Hugo_Symbol o.tsv
args <- commandArgs(T)
t1 <- read.delim(file = args[1], header = TRUE, sep = '\t', na.strings = c('', '.', 'NA'))
t2 <- read.delim(file = args[2], header = TRUE, sep = '\t', na.strings = c('', '.', 'NA'))
join_colname <- args[3]  # join_colname <- c('Hugo_Symbol')
output_file <- args[4]

# NOTE: need to make sure there are no duplicate names or it will cause duplicate output entries
t1_cols <- colnames(t1)[! colnames(t1) %in% join_colname]
t2_cols <- colnames(t2)[! colnames(t2) %in% join_colname]
common_cols <- intersect(t1_cols, t2_cols)
if (length(common_cols) > 0){
    stop(paste(c("ERROR: input tables have common columns; ", common_cols), collapse = ' '))
}

# merge the two tables
t3 <- merge(x = t1, y = t2, by = join_colname, all = TRUE)
write.table(x = t3, file = output_file, quote = FALSE, sep = '\t', row.names = FALSE, col.names = TRUE)

