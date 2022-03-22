#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Basic use case; write a column with msi status to a table
Usage:
python3 bin/add_msi_status.py -i input_file.tsv -o output_file.tsv --header my_header

-----
NOTE: MOVE MAF OUTPUT AND FORMATTER TO cBioPortal_utils.MafWriter !! DO NOT ADD MORE ONE-OFF MAF FORMATTING MODULES AND METHODS !!
-----
"""
import os,sys,csv,argparse
from cBioPortal_utils import MafReader

def calc_msi(msi_score):
    msi_score = float(msi_score)
    msi_type = 'NA' # default value ; also applies for nan values
    if msi_score < 3:
        msi_type = 'Stable'
    elif msi_score >= 3 and msi_score < 10:
        msi_type = 'Indeterminate'
    elif msi_score >= 10:
        msi_type = 'Instable'
    return msi_type


def main(**kwargs):
    """
    Paste the column on the file
    """
    input_file = kwargs.pop('input_file', None)
    output_file = kwargs.pop('output_file', None)
    delim = kwargs.pop('delim', '\t')
    header = kwargs.pop('header', None)

    if input_file:
        fin = open(input_file)
    else:
        fin = sys.stdin

    if output_file:
        fout = open(output_file, "w")
    else:
        fout = sys.stdout

    if header:
        old_header = next(fin).strip()
        new_header = old_header + delim + header + '\n'
        fout.write(new_header)


    maf_reader = MafReader(input_file)

    # write analysis files
    with open(output_file,'w') as fout:
        fieldnames = maf_reader.get_fieldnames()

        # add the new columns labels for output
        fieldnames.append(header)

        # start output csv parser
        # ignore fields not in fieldnames
        # NOTE: csv writer includes carriage returns that we dont want
        # https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
        writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = fieldnames, extrasaction = 'ignore', lineterminator='\n')
        writer.writeheader()

        # update each input row and write it to output
        for row in maf_reader.read():
            msi_status = calc_msi(row['MSI_SCORE'])
            row[header] = msi_status
            writer.writerow(row)


def parse():
    """
    Parses script args
    """
    parser = argparse.ArgumentParser(description='Append a column of text to a file with msi status based on the msi value')
    parser.add_argument("-i", default = None, dest = 'input_file', help="Input file")
    parser.add_argument("-o", default = None, dest = 'output_file', help="Output file")
    parser.add_argument("-d", default = '\t', dest = 'delim', help="Delimiter")
    parser.add_argument("--header", default = None, dest = 'header', help="Header for the msi status column")
    args = parser.parse_args()

    main(**vars(args))

if __name__ == '__main__':
    parse()
