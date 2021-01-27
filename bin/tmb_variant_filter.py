#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to filter variant .maf file to use with TMB tumor mutational burden calculation
"""
import csv
import sys
from cBioPortal_utils import MafReader, is_TERT_promoter

alt_dp_colname = 't_alt_count'
ref_dp_colname = 't_ref_count'
af_colname = 't_af'
frequency_min = 0.05

dp_colname = 't_depth'
coverage_min = 500.0

gene_function_colname = 'Consequence'
gene_function_exclude = set(['synonymous_variant'])
# gene_function_allowed = # ['exonic'] # Func_refGene_allowed

mutation_status_colname = 'Mutation_Status'
mutation_status_exclude = set(['GERMLINE', 'UNKNOWN'])

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

def get_af(row):
    """
    Get the allele frequency from the row or calculate it if missing
    """
    try:
        # af col is present; t_af
        af = float(row[af_colname])
    except KeyError:
        # get the values needed to calculate Depth, so that we can calculate AF
        dp = row.get(dp_colname) # 't_depth'
        alt_dp = row.get(alt_dp_colname) # 't_alt_count'
        ref_df = row.get(ref_dp_colname) # 't_ref_count'

        # need to coerce to int
        try:
            dp = int(dp)
        # it was not a valid value to coerce to int
        except ValueError:
            dp = int(alt_dp) + int(ref_df)
        except TypeError:
            dp = int(alt_dp) + int(ref_df)

        af = float( int(alt_dp) / dp )
    return(af)

def get_dp(row):
    """
    Handling to try and get the depth value from the row
    """
    try:
        dp = row.get(dp_colname) # 't_depth'
        dp = float(dp) # 't_depth'
    # it was not a valid value to coerce to int
    except ValueError:
        # the column is not a valid int; try a different col instead
        alt_dp = row.get(alt_dp_colname) # 't_alt_count'
        ref_df = row.get(ref_dp_colname) # 't_ref_count'
        dp = int(alt_dp) + int(ref_df)
    except TypeError:
        alt_dp = row.get(alt_dp_colname) # 't_alt_count'
        ref_df = row.get(ref_dp_colname) # 't_ref_count'
        dp = int(alt_dp) + int(ref_df)
    return(dp)

def filter_row(row):
    """
    Evaluate values in the row to decide if it should be included (True) or excluded (False) from the output

    Need to report mutations that are NOT synonymous_variant EXCEPT for TERT promoter
    """
    keep_row = True
    af = get_af(row)
    dp = get_dp(row)
    mutation_status = row.get(mutation_status_colname, None)
    gene_function_str = row[gene_function_colname]
    gene_functions = set(gene_function_str.split(','))

    tert = is_TERT_promoter(row,
        start_ge = 1295141, # start pos must be greater than or equal to this
        start_le = 1295340) # start pos must be less than or equal to this
    """
    NOTE: these coordinates are only for B37

    it matters whether the event is _on_ or _off_ target. Only certainly capture assays have probes for the TERT promoter. So if you only want to label _on_ target events you would need to check for that.

    For TMB you for sure only want to count _on_ target events as you are going to be measuring a density (#events / target area).
    """

    if af < frequency_min:
        keep_row = False

    if dp < coverage_min:
        keep_row = False

    if mutation_status is not None:
        if mutation_status.upper() in mutation_status_exclude:
            keep_row = False

    # if gene_functions are in the gene_function_exclude list;
    # report only if mut is NOT synonymous_variant...
    if gene_function_exclude.intersection(gene_functions):
        """
        >>> excl = set([3])
        >>> x = set([1,2])
        >>> excl.intersection(x)
        set()
        >>> z = set([3,4])
        >>> excl.intersection(z)
        {3}
        """
        # ... EXCEPT for TERT promoter
        if not tert:
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
