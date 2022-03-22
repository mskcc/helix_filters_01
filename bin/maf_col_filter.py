#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for dropping specific columns from a given maf file

NOTE: MOVE MAF OUTPUT AND FORMATTER TO cBioPortal_utils.MafWriter !!
"""
import sys
import csv

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .cBioPortal_utils import MafReader

if __name__ == "__main__":
    from cBioPortal_utils import MafReader

# list of column labels that we will preserve in the output; discard any columns not listed here
# NOTE: set does not preserve order but is faster for lookups
cols_to_keep = set([
"Hugo_Symbol",
"Entrez_Gene_Id",
"Center",
"NCBI_Build",
"Chromosome",
"Start_Position",
"End_Position",
"Strand",
"Variant_Classification",
"Variant_Type",
"Reference_Allele",
"Tumor_Seq_Allele1",
"Tumor_Seq_Allele2",
"dbSNP_RS",
"dbSNP_Val_Status",
"Tumor_Sample_Barcode",
"Matched_Norm_Sample_Barcode",
"Match_Norm_Seq_Allele1",
"Match_Norm_Seq_Allele2",
"Tumor_Validation_Allele1",
"Tumor_Validation_Allele2",
"Match_Norm_Validation_Allele1",
"Match_Norm_Validation_Allele2",
"Verification_Status",
"Validation_Status",
"Mutation_Status",
"Sequencing_Phase",
"Sequence_Source",
"Validation_Method",
"Score",
"BAM_File",
"Sequencer",
"Tumor_Sample_UUID",
"Matched_Norm_Sample_UUID",
"HGVSc",
"HGVSp",
"Amino_Acid_Change", # added by maf_filter script so not in raw maf
"Transcript_ID",
"Exon_Number",
"t_depth",
"t_ref_count",
"t_alt_count",
"n_depth",
"n_ref_count",
"n_alt_count",
"t_af", # added by the add_af.py script
"is_in_impact", # added by the add_is_in_impact.py script
"impact_assays"
])

def main(input_file, output_file):
    """
    Main control function for the script
    """
    maf_reader = MafReader(input_file)
    fieldnames = maf_reader.get_fieldnames()
    comment_lines = maf_reader.comment_lines

    # only keep a subset of the fieldnames for the shareable output file
    fieldnames = [ f for f in fieldnames if f in cols_to_keep ]

    with open(output_file, "w") as fout:
        # write out the input comments
        fout.writelines(comment_lines)

        # ignore fields not in fieldnames
        writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = fieldnames, extrasaction = 'ignore', lineterminator='\n')
        writer.writeheader()

        # write out the input rows
        for row in maf_reader.read():
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
