#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for dropping specific columns from a given maf file
"""
import sys
import csv

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .cBioPortal_utils import parse_header_comments

if __name__ == "__main__":
    from cBioPortal_utils import parse_header_comments


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
"n_alt_count"
])

def main(input_file, output_file):
    """
    Main control function for the script
    """
    # get the comments from the file and find the beginning of the table header
    comments, start_line = parse_header_comments(input_file)
    comments_lines = [ c + '\n' for c in comments ]

    with open(input_file,'r') as fin, open(output_file, "w") as fout:
        # skip comment lines
        while start_line > 0:
            next(fin)
            start_line -= 1

        reader = csv.DictReader(fin, delimiter = '\t')
        fieldnames = reader.fieldnames

        # only keep a subset of the fieldnames for the shareable output file
        fieldnames = [ f for f in fieldnames if f in cols_to_keep ]

        fout.writelines(comments_lines)
        # ignore fields not in fieldnames
        writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = fieldnames, extrasaction = 'ignore', lineterminator='\n')
        writer.writeheader()
        for row in reader:
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
