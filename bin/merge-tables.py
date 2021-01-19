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
from cBioPortal_utils import TableReader, create_file_lines

def write_table(
    comments, # list of comment lines
    fieldnames, # list of output fieldnames
    delimiter,
    rows, # list of dict rows to write
    fout # file output handle
    ):
    # write the output table
    for line in comments:
        fout.write(line)

    # start csv writer
    writer = csv.DictWriter(fout, delimiter = delimiter, fieldnames = fieldnames)
    writer.writeheader()

    # write table rows;
    for row in rows:
        writer.writerow(row)


def merge_comments(
    comments1, # list of comment line strings
    comments2 # list of comment line strings
    ):
    """
    Merge together all the comment lines from the tables
    """
    all_comments = [ *comments1, *comments2 ]
    return(all_comments)

def merge_records(
    records1, # list of rows (dicts) from the first table
    records2, # list of rows (dicts) from the second table
    key1, # first table merge key
    key2 # second table merge key
    ):
    """
    Merge the records from the two tables

    merged_records, merged_rows = merge_records(records1, records2, key1, key2)
    """
    # start a new map for the records
    records = OrderedDict()

    # update the map for the values in the first table by key
    # NOTE: if tables are huge consider changing this to a `while len(recs) > 0: rec = recs.pop(); ...` so we dont have multiple copies of the entire dataset in memory at once
    for rec in records1:
        key = rec.pop(key1)
        records[key] = rec

    # add the matching row in the second table
    for rec in records2:
        key = rec.pop(key2)
        records[key] = {**records[key], **rec}
    """
    looks like this;

    >>> records
    odict_items([
    ('Sample1', {'PATIENT_ID': 'Patient1', 'SAMPLE_COVERAGE': '108', 'TMB': '100'}),
    ('Sample2', {'PATIENT_ID': 'Patient2', 'SAMPLE_COVERAGE': '502', 'TMB': '200'}),
    ('Sample3', {'PATIENT_ID': 'Patient3', 'SAMPLE_COVERAGE': '256', 'TMB': '300'})
    ])
    """

    # collapse the merged records back into rows;
    rows = []
    for key, rec in records.items():
        row = {}
        row[key1] = key
        row = {**row, **rec}
        rows.append(row)
    """
    looks like this;

    >>> rows
    [
    {'SAMPLE_ID': 'Sample1', 'PATIENT_ID': 'Patient1', 'SAMPLE_COVERAGE': '108', 'CMO_TMB_SCORE': '100'},
    {'SAMPLE_ID': 'Sample2', 'PATIENT_ID': 'Patient2', 'SAMPLE_COVERAGE': '502', 'CMO_TMB_SCORE': '200'},
    {'SAMPLE_ID': 'Sample3', 'PATIENT_ID': 'Patient3', 'SAMPLE_COVERAGE': '256', 'CMO_TMB_SCORE': '300'}
    ]
    """
    return(records, rows)

def generate_output_fieldnames(fieldnames1, fieldnames2, key2):
    """
    get the output column headers; exclude key2
    """
    output_fieldnames = [ f for f in fieldnames1 ]
    output_fieldnames = [ *output_fieldnames, *[f for f in fieldnames2 if f!= key2] ]
    return(output_fieldnames)

def merge_standard_tables(
    comments1,
    comments2,
    records1,
    records2,
    key1,
    key2,
    fieldnames1,
    fieldnames2,
    delimiter,
    fout
    ):
    """
    Merge operation on standard tsv tables
    """
    # Concatenate all the comment lines; these will still have trailing '\n' !!
    all_comments = merge_comments(comments1, comments2)

    # combine the records from the two tables
    _, merged_rows = merge_records(records1, records2, key1, key2)

    # get the output column headers; exclude key2
    output_fieldnames = generate_output_fieldnames(fieldnames1, fieldnames2, key2)

    # write the output table
    write_table(all_comments, output_fieldnames, delimiter, merged_rows, fout)

def merge_cBioPortal_tables(records1, records2, key1, key2, fieldnames1, fieldnames2, delimiter, fout):
    """
    Merges the records of two tables and outputs the result in a cBioPortal compatible format;
    The header comment lines from both tables are ignored and new comments are generated for use with cBioPortal
    """
    # combine the records from the two tables
    _, merged_rows = merge_records(records1, records2, key1, key2)

    # get the output column headers; exclude key2
    output_fieldnames = generate_output_fieldnames(fieldnames1, fieldnames2, key2)

    # convert the rows into cBioPortal file lines
    lines = create_file_lines(merged_rows, delimiter)

    # write the lines
    fout.writelines(lines)

def merge_tables(
    table1,
    table2,
    key1,
    key2,
    output_file = None,
    delimiter = '\t',
    cBioPortal = False,
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
    comments1 = table1_reader.comment_lines
    fieldnames1 = table1_reader.get_fieldnames()
    records1 = [ rec for rec in table1_reader.read() ]

    table2_reader = TableReader(table2, delimiter = delimiter)
    comments2 = table2_reader.comment_lines
    fieldnames2 = table2_reader.get_fieldnames()
    records2 = [ rec for rec in table2_reader.read() ]

    if cBioPortal:
        merge_cBioPortal_tables(
            records1,
            records2,
            key1,
            key2,
            fieldnames1,
            fieldnames2,
            delimiter,
            fout
        )
    else:
        merge_standard_tables(
            comments1,
            comments2,
            records1,
            records2,
            key1,
            key2,
            fieldnames1,
            fieldnames2,
            delimiter,
            fout
        )

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
    parser.add_argument('--cBioPortal', dest = 'cBioPortal', action = "store_true", help = 'Ignore header comment lines and output table with cBioPortal headers. NOTE: all output header columns must be supported in cBioPortal_utils.header_lines_map')
    parser.set_defaults(func = merge_tables)
    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    main()
