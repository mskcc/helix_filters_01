#!/usr/bin/env python3
"""
Script to add column for t_af tumor variant allele frequency to the maf file

To calculate vaf, we can use the same columns we give to the portal, which should be t_depth and t_alt_count

tumor_AF = t_alt_count / t_depth

-----
NOTE: MOVE MAF OUTPUT AND FORMATTER TO cBioPortal_utils.MafWriter !! DO NOT ADD MORE ONE-OFF MAF FORMATTING MODULES AND METHODS !!
-----
"""
import sys
import csv
from cBioPortal_utils import MafReader

def main(input_file, output_file):
    """
    Main control function for the script
    """
    maf_reader = MafReader(input_file)
    fieldnames = maf_reader.get_fieldnames()
    comment_lines = maf_reader.comment_lines

    # add the AF column label
    fieldnames.append('t_af')

    with open(output_file, "w") as fout:
        # write out the input comments
        fout.writelines(comment_lines)

        # ignore fields not in fieldnames
        writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = fieldnames, extrasaction = 'ignore', lineterminator='\n')
        writer.writeheader()

        # write out the input rows
        for row in maf_reader.read():
            # NOTE: In Python 2, division of two ints produces an int. In Python 3, it produces a float.
            row['t_af'] = float(int(row['t_alt_count']) / int(row['t_depth']))
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
