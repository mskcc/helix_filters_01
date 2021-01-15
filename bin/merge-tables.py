#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to merge tables together based on rows
"""
import sys
import argparse
import csv
from collections import OrderedDict
from functools import reduce
from cBioPortal_utils import TableReader

def merge_tables(
    table1,
    table2,
    key1,
    key2,
    output_file = None,
    delimiter = '\t',
    func = None):
    """
    Merge two tables on rows in a common column
    """
    # open output file
    if output_file:
        fout = open(output_file, "w")
    else:
        fout = sys.stdout

    # load all records from both tables
    table1_reader = TableReader(table1, delimiter = delimiter)
    table1_comment_lines = table1_reader.comment_lines
    table1_fieldnames = table1_reader.get_fieldnames()
    table1_records = [ rec for rec in table1_reader.read() ]

    table2_reader = TableReader(table2, delimiter = delimiter)
    table2_comment_lines = table2_reader.comment_lines
    table2_fieldnames = table2_reader.get_fieldnames()
    table2_records = [ rec for rec in table2_reader.read() ]

    # Concatenate all the comment lines; these will still have trailing '\n' !!
    all_comments = [ *table1_comment_lines, *table2_comment_lines ]

    # start a new map for the records
    merged_records = OrderedDict()

    # update the map for the values in the first table by key
    # NOTE: if tables are huge consider changing this to a `while len(recs) > 0: rec = recs.pop(); ...` so we dont have multiple copies of the entire dataset in memory at once
    for rec in table1_records:
        key = rec.pop(key1)
        merged_records[key] = rec

    # add the matching row in the second table
    for rec in table2_records:
        key = rec.pop(key2)
        merged_records[key] = {**merged_records[key], **rec}

    # collapse the merged records back into rows;
    # get the output column headers; exclude key2
    output_fieldnames = [ f for f in table1_fieldnames ]
    output_fieldnames = [ *output_fieldnames, *[f for f in table2_fieldnames if f!= key2] ]

    # write the output table
    for line in all_comments:
        fout.write(line)
    writer = csv.DictWriter(fout, delimiter = delimiter, fieldnames = output_fieldnames)
    writer.writeheader()
    for key, rec in merged_records.items():
        row = {}
        row[key1] = key
        row = {**row, **rec}
        writer.writerow(row)

    fout.close()


def main():
    """
    Parse command line arguments to run the script
    """
    parser = argparse.ArgumentParser(description = 'Merge tables together by rows. Tables must have column headers. Values in the key column must be unique.')
    parser.add_argument('table1', help = 'First table to merge against')
    parser.add_argument('table2', help = 'Second table to merge against')
    parser.add_argument('--key1', dest = 'key1', required = True, help = 'Column label to use for merge in first table')
    parser.add_argument('--key2', dest = 'key2', required = True, help = 'Column label to use for merge in second table')
    parser.add_argument('--output', dest = 'output_file', help = 'Name of the output file')
    parser.set_defaults(func = merge_tables)
    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    main()
