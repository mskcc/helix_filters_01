#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Concatenates supplied input table files, filling in missing columns between files

Notes
-----
All tables should have the same delimiter. No single table should have duplicated column names (e.g. file1.tsv and file2.tsv can share column names, but each column in file1.tsv should have a unique header, etc.)

Examples
--------
Example usage::

    ./concat-tables.py -o concat.tsv NC-HAPMAP.HaplotypeCaller.annotations.tsv NC-HAPMAP.LoFreq.annotations.tsv

"""
import csv
import sys
from collections import OrderedDict
import argparse

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)
"""
https://stackoverflow.com/questions/14207708/ioerror-errno-32-broken-pipe-python
"""

def find_start_line(filename, comment_char = '#'):
    """
    Find the first non-comment line in the file
    """
    start_line = 0
    with open(filename) as fin:
        for i, line in enumerate(fin):
            if line.startswith('#'):
                start_line += 1
    return(start_line)

def get_all_comments(files, comment_char = '#'):
    """
    Retrives all the unique pre-header comment lines from all the files in the list
    """
    comments = []
    for f in files:
        with open(f) as fin:
            for line in fin:
                if line.startswith(comment_char):
                    comment = line.strip()
                    if comment not in comments:
                        comments.append(comment)
                else:
                    break
    return(comments)

def get_all_fieldnames(files, delimiter, has_comments = False, comment_char = '#'):
    """
    Retrieves all the column names from all files in the list

    Paramters
    ---------
    files: list
        a list of paths to input files
    delimiter: str
        the delimiter to use for the input files

    Returns
    -------
    list
        a list of column names amongst all the files

    Notes
    -----
    The column names will be returned in the following order: all columns from the first file, then each missing column from all subsequent files.
    """
    fieldnames = OrderedDict()
    for f in files:
        with open(f) as fin:
            if has_comments:
                start_line = find_start_line(f, comment_char = comment_char)
                while start_line > 0:
                    next(fin)
                    start_line -= 1
            reader = csv.DictReader(fin, delimiter = delimiter)
            for name in reader.fieldnames:
                fieldnames[name] = ''
    return(fieldnames.keys())

def update_dict(d, keys, default_val):
    """
    Checks that all provided fieldnames exist as keys in the dict, and if they are missing creates them with the default value

    Parameters
    ----------
    d: dict
        a dictionary to be updated
    keys: list
        a list of keys to check in the dict
    default_val: str
        a default value to initialize the missing keys to

    Returns
    -------
    dict
        a dictionary with the updated keys
    """
    for key in keys:
        if not d.get(key, None):
            d[key] = default_val
    return(d)

def main(**kwargs):
    """
    Main control function for the script
    """
    input_files = kwargs.pop('input_files')
    output_file = kwargs.pop('output_file', None)
    delimiter = kwargs.pop('delimiter', '\t')
    na_str = kwargs.pop('na_str', '.')
    has_comments = kwargs.pop('has_comments', False)
    comment_char = kwargs.pop('comment_char', '#')

    comments = None
    if has_comments:
        comments = get_all_comments(files = input_files, comment_char = comment_char)

    output_fieldnames = get_all_fieldnames(files = input_files, delimiter = delimiter, has_comments = has_comments, comment_char = comment_char)

    if output_file:
        fout = open(output_file, "w")
    else:
        fout = sys.stdout

    if comments:
        for comment in comments:
            fout.write(comment + '\n')

    writer = csv.DictWriter(fout, delimiter = delimiter, fieldnames = output_fieldnames)
    writer.writeheader()
    for input_file in input_files:
        with open(input_file) as fin:
            if has_comments:
                start_line = find_start_line(input_file, comment_char = comment_char)
                while start_line > 0:
                    next(fin)
                    start_line -= 1
            reader = csv.DictReader(fin, delimiter = delimiter)
            for row in reader:
                row = update_dict(d = row, keys = output_fieldnames, default_val = na_str)
                try:
                    writer.writerow(row)
                except ValueError as err:
                    # if there were comment lines in one of the input files and the script was run without `--comments` and has_comments=True, then the resulting row dict will often have the wrong keys set due to misreading the file header line, including a None key with all the intended columns
                    # see "extrasaction='raise'" here: https://docs.python.org/3/library/csv.html#csv.DictWriter
                    # >>> print([k for k in row.keys() if k not in output_fieldnames])
                    raise Exception('Could not write row, are there columns without headers or comment lines included?') from err

    fout.close()



def parse():
    """
    Parses script args
    """
    parser = argparse.ArgumentParser(description='Concatenates tables')
    parser.add_argument('input_files', nargs='*', help="Input files")
    parser.add_argument("-o", default = None, dest = 'output_file', help="Output file")
    parser.add_argument("-d", default = '\t', dest = 'delimiter', help="Delimiter")
    parser.add_argument("-n", default = '.', dest = 'na_str', help="NA string; character to insert for missing fields in table")
    parser.add_argument("--comments", action='store_true', dest = 'has_comments', help="Whether the input files have comment lines preceeding the header; they will be retained in the output")
    parser.add_argument("--comment-char", default = '#', dest = 'comment_char', help="Character for comment lines")
    args = parser.parse_args()

    main(**vars(args))

if __name__ == '__main__':
    parse()
