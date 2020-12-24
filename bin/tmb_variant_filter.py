#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to filter variant .maf file to use with TMB calculation
"""
import csv
import sys
from cBioPortal_utils import MafReader

# alt_dp_colname = 't_alt_count'
af_colname = 't_af'
frequency_min = 0.05

dp_colname = 't_depth'
coverage_min = 500.0

gene_function_colname = 'Consequence'
gene_function_exclude = set(['synonymous_variant'])
# gene_function_allowed = # ['exonic'] # Func_refGene_allowed

# Variant_Classification
# ----------------------
# Silent
# Missense_Mutation
# Splice_Region
# Nonstop_Mutation
# Translation_Start_Site
# Nonsense_Mutation
# Splice_Site
# 5'Flank
# Frame_Shift_Ins
# Frame_Shift_Del
# In_Frame_Del

# Consequence
# -----------
# synonymous_variant
# missense_variant
# splice_region_variant,intron_variant
# stop_lost
# start_lost
# stop_gained
# missense_variant,splice_region_variant
# splice_acceptor_variant
# splice_region_variant,synonymous_variant
# stop_gained,splice_region_variant
# splice_donor_variant
# upstream_gene_variant
# frameshift_variant
# splice_region_variant,3_prime_UTR_variant
# stop_retained_variant
# inframe_deletion
# splice_region_variant,5_prime_UTR_variant

def filter_row(row):
    """
    Evaluate values in the row to decide if it should be included (True) or excluded (False) from the output
    """
    keep_row = True
    af = float(row[af_colname])
    dp = float(row[dp_colname])
    gene_function_str = row[gene_function_colname]
    gene_functions = set(gene_function_str.split(','))

    if af < frequency_min:
        keep_row = False

    if dp < coverage_min:
        keep_row = False

    if gene_function_exclude.intersection(gene_functions):
        keep_row = False

    return(keep_row)

def main(input_file, output_file):
    """
    Main control function for the script
    """
    # setup reader from the input maf file
    maf_reader = MafReader(input_file)
    fieldnames = maf_reader.get_fieldnames()
    comment_lines = maf_reader.comment_lines


    with open(output_file, "w") as fout:
        # write out the input comments
        fout.writelines(comment_lines)

        # ignore fields not in fieldnames
        writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = fieldnames, extrasaction = 'ignore', lineterminator='\n')
        writer.writeheader()

        # write out the input rows that pass filter criteria
        for row in maf_reader.read():
            if filter_row(row):
                writer.writerow(row)

def parse():
    """
    Parse command line options
    """
    args = sys.argv[1:]
    input_file = args[0]
    output_file = args[1]
    main(input_file, output_file)

if __name__ == '__main__':
    parse()
