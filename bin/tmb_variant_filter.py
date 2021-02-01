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
# NOTE: frequency_min *must* be >0.0 or else invalid variant calls might get through!! Some discrepant variants have been seen with ref and alt allele counts of 0 and no 'depth' value recorded

dp_colname = 't_depth'
coverage_min = 500.0

gene_function_colname = 'Consequence'
gene_function_exclude = set(['synonymous_variant'])
# gene_function_allowed = # ['exonic'] # Func_refGene_allowed

mutation_status_colname = 'Mutation_Status'
mutation_status_exclude = set(['GERMLINE', 'UNKNOWN'])

# Variant_Classification known values;
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

# Consequence known values;
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

def get_ref_alt_depth(row):
    """
    Handler to try and retrieve the tumor variant allele ref and alt depths, and the overall variant depth, from the row
    Need to handle missing and messed up values
    """
    keys = [
        alt_dp_colname, # 't_alt_count'
        ref_dp_colname, # 't_ref_count'
        dp_colname, # 't_depth'
    ]
    values = {}
    for key in keys:
        # get the value if its present
        values[key] = row.get(key, None)
        # try to convert it to an int
        try:
            values[key] = int(values[key])
        # not a valid int
        except TypeError:
            values[key] = None
        except ValueError:
            values[key] = None

    ref_count = values[ref_dp_colname]
    alt_count = values[alt_dp_colname]
    depth = values[dp_colname]

    if depth is None:
        # try to calculate from the other two values
        if ref_count is not None and alt_count is not None:
            depth = ref_count + alt_count

    return(ref_count, alt_count, depth)

def calc_af(ref_count, alt_count, depth):
    """
    Calculate the af from value provided
    """
    af = 0.0 # default value in case some of the input values are bad
    if depth and alt_count: # non-0 or not None
        af = float( alt_count / depth )
    elif ref_count and alt_count:
        depth = int( ref_count + alt_count )
        af = float( alt_count / depth )
    return(af)


def filter_row(row):
    """
    Evaluate values in the row to decide if it should be included (True) or excluded (False) from the output

    Need to report mutations that are NOT synonymous_variant EXCEPT for TERT promoter
    """
    keep_row = True
    ref_count, alt_count, depth = get_ref_alt_depth(row)

    if af_colname in row:
        try:
            af = float(row[af_colname])
        except TypeError:
            af = calc_af(ref_count, alt_count, depth)
        except ValueError:
            af = calc_af(ref_count, alt_count, depth)
    else:
        af = calc_af(ref_count, alt_count, depth)

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

    # immediately quit on these conditions
    if not depth:
        return(False)

    if depth < coverage_min:
        return(False)

    if not af:
        return(False)

    if af < frequency_min:
        return(False)


    # check multiple criteria for these conditions
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
