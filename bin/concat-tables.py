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
import os
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
            if line.startswith(comment_char):
                start_line += 1
    return(start_line)

def get_all_comments(files, comment_char = '#', progress = False):
    """
    Retrives all the unique pre-header comment lines from all the files in the list
    """
    num_files = len(files)
    comments = []
    for i, f in enumerate(files):
        if progress:
            show_progress(
                prefix = 'Parsing comments ',
                num_done = i,
                num_total = num_files,
                current_item = f
                )
        with open(f) as fin:
            for line in fin:
                if line.startswith(comment_char):
                    comment = line.strip()
                    if comment not in comments:
                        comments.append(comment)
                else:
                    break
    if progress:
        show_progress(clear = True)
    return(comments)

def get_all_fieldnames(files, delimiter, has_comments = False, comment_char = '#', progress = False):
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
    num_files = len(files)
    for i, f in enumerate(files):
        if progress:
            show_progress(
                prefix = 'Parsing fieldnames ',
                num_done = i,
                num_total = num_files,
                current_item = f
                )
        with open(f) as fin:
            if has_comments:
                start_line = find_start_line(f, comment_char = comment_char)
                while start_line > 0:
                    next(fin)
                    start_line -= 1
            reader = csv.DictReader(fin, delimiter = delimiter)
            for name in reader.fieldnames:
                fieldnames[name] = ''
    if progress:
        show_progress(clear = True)
    return(fieldnames.keys())

def update_dict(d, keys, default_val, keep_keys = False, na_keys = False):
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
    keep_keys: bool | set
        a set() of keys that should be retained, exclude all others
    na_keys: bool | set
        a set() of keys that should have their value changed to `default_val`

    Returns
    -------
    dict
        a dictionary with the updated keys
    """
    # NOTE: I think Python defaults to pass by reference here; be careful with this,
    # might need to use copy.deepcopy in the future to avoid issues with passing around modified dicts
    for key in keys:
        if not d.get(key, None):
            d[key] = default_val
    if keep_keys:
        d = { k:v for k,v in d.items() if k in keep_keys }
    if na_keys:
        for key in na_keys:
            d[key] = default_val
    return(d)

def get_files_from_dir(input_dirs):
    """
    Get the files from a directory
    I think this should only search one level deep
    """
    files = []
    for input_dir in input_dirs:
        for dirpath, dirnames, filenames in os.walk(input_dir):
            for filename in filenames:
                path = os.path.join(dirpath, filename)
                files.append(path)
    return(files)

def get_files_from_lists(input_files):
    """
    Read the file paths from the input files and return the list of all file paths
    """
    files = []
    for input_file in input_files:
        with open(input_file) as fin:
            for line in fin:
                files.append(line.strip())
    return(files)

def show_progress(num_done = 0, num_total = 1, current_item = None, prefix = '', fout = sys.stderr, clear = False):
    """
    Prints the progress to the console

    NOTE: for some reason this always stops 1 short but still says 100%, not sure why
    """
    if clear:
        fout.write('\n')
        return()
    pcnt = round(float(num_done / num_total) * 100, 1)
    text = "{}{}% ({}/{})\r".format(prefix, pcnt, num_done, num_total)
    fout.write(text)
    fout.flush()

def main(**kwargs):
    """
    Main control function for the script

    TODO: wrap the main script logic in a generator function so that it could be imported and used directly in Python easier
    """
    input_files = kwargs.pop('input_files')
    output_file = kwargs.pop('output_file', None)
    delimiter = kwargs.pop('delimiter', '\t')
    na_str = kwargs.pop('na_str', '.')
    has_comments = kwargs.pop('has_comments', False)
    comment_char = kwargs.pop('comment_char', '#')
    dir = kwargs.pop('dir', False)
    filenames = kwargs.pop('filenames', False)
    filename_header = kwargs.pop('filename_header', 'file') # NOTE: things will prob break if there's already a column with this header so watch out for that
    progress = kwargs.pop('progress', False)
    from_list = kwargs.pop('from_list', False)
    keep_cols = kwargs.pop('keep_cols', set())
    na_cols = kwargs.pop('na_cols', set())

    if keep_cols is None:
        keep_cols = set()
    else:
        keep_cols = set(keep_cols)

    if na_cols is None:
        na_cols = set()
    else:
        na_cols = set(na_cols)

    # treat the input files as directories of files for concat'ing
    if dir:
        if progress:
            sys.stderr.write('Finding input files in dir\n')
        input_files = get_files_from_dir(input_dirs = input_files)
        if progress:
            sys.stderr.write('Found {} files\n'.format(len(input_files)))

    # treat the input files as lists of file paths to read for input
    if from_list:
        if progress:
            sys.stderr.write('Finding input files from lists\n')
        input_files = get_files_from_lists(input_files = input_files)
        if progress:
            sys.stderr.write('Found {} files\n'.format(len(input_files)))

    # get the comment lines from each input file, in order, if we are parsing comments
    comments = None
    if has_comments:
        comments = get_all_comments(files = input_files, comment_char = comment_char, progress = progress)

    # get the output header column fieldnames, in order, from all the input files
    output_fieldnames = get_all_fieldnames(
        files = input_files,
        delimiter = delimiter,
        has_comments = has_comments,
        comment_char = comment_char,
        progress = progress)

    # remove some colnames
    if keep_cols:
        output_fieldnames = [ f for f in output_fieldnames if f in keep_cols ]

    # add cols that should have NA value if they are missing
    if na_cols:
        for colname in na_cols:
            if colname not in output_fieldnames:
                output_fieldnames.append(colname)

    # add an extra column if we are keeping filenames in the output
    if filenames:
        output_fieldnames = [ *output_fieldnames, filename_header ]

    # initialize output file handle
    if output_file:
        fout = open(output_file, "w")
    else:
        fout = sys.stdout

    # if we had comments we need to write them out to the file handle
    if comments:
        for comment in comments:
            fout.write(comment + '\n')

    # initialize output parser
    writer = csv.DictWriter(fout, delimiter = delimiter, fieldnames = output_fieldnames)
    writer.writeheader()

    # parse the rest of each input file
    num_files = len(input_files)
    num_files_done = 0
    for input_file in input_files:
        # show the progress bar
        if progress:
            show_progress(
                prefix = 'Parsing rows ',
                num_done = num_files_done,
                num_total = num_files,
                current_item = input_file
                )

        with open(input_file) as fin:
            # skip comment lines to find the first header line, if we are parsing comments
            if has_comments:
                start_line = find_start_line(input_file, comment_char = comment_char)
                while start_line > 0:
                    next(fin)
                    start_line -= 1

            # start parsing the file
            reader = csv.DictReader(fin, delimiter = delimiter)
            for row in reader:
                # make sure all the desired output fields are present in each row
                row = update_dict(
                    d = row,
                    keys = output_fieldnames,
                    default_val = na_str,
                    keep_keys = keep_cols,
                    na_keys = na_cols)
                # if we're keeping filenames then add that value here
                if filenames:
                    row[filename_header] = input_file
                try:
                    writer.writerow(row)
                except ValueError as err:
                    # if there were comment lines in one of the input files and the script was run without `--comments` and has_comments=True, then the resulting row dict will often have the wrong keys set due to misreading the file header line, including a None key with all the intended columns
                    # see "extrasaction='raise'" here: https://docs.python.org/3/library/csv.html#csv.DictWriter
                    # >>> print([k for k in row.keys() if k not in output_fieldnames])
                    raise Exception('Could not write row, are there columns without headers or comment lines included?') from err
        num_files_done += 1

    fout.close()



def parse():
    """
    Parses script args
    """
    parser = argparse.ArgumentParser(description='Concatenates tables')
    parser.add_argument('input_files', nargs='*', help="Input files")
    parser.add_argument("-o", default = None, dest = 'output_file', help="Output file")
    parser.add_argument("-d", default = '\t', dest = 'delimiter', help="Delimiter")
    parser.add_argument("-n", '--na-str', default = '.', dest = 'na_str', help="NA string; character to insert for missing fields in table")
    parser.add_argument("--comments", action='store_true', dest = 'has_comments', help="Whether the input files have comment lines preceeding the header; they will be retained in the output")
    parser.add_argument("--comment-char", default = '#', dest = 'comment_char', help="Character for comment lines")
    parser.add_argument("--dir", action = 'store_true', dest = 'dir', help="Input file is a directory")
    parser.add_argument("--filenames", action = 'store_true', dest = 'filenames', help="Write out an extra column with the input filename from each row")
    parser.add_argument("--filename-header", default = 'file', dest = 'filename_header', help="If outputting filenames, use this value as the header for the column")
    parser.add_argument("--from-list", action = 'store_true', dest = 'from_list', help="Treat each input file as a file list containing the paths to all the files to be concatenated")
    parser.add_argument("--progress", action = 'store_true', dest = 'progress', help="Show progress bar")
    parser.add_argument("--keep-cols", nargs = '*', dest = 'keep_cols', help="List of columns to keep in the output file; all other columns will be removed, missing columns will be created with NA str")
    parser.add_argument("--na-cols", nargs = '*', dest = 'na_cols', help="List of columns to keep in the output file but replace their values with the NA str")

    args = parser.parse_args()

    main(**vars(args))

if __name__ == '__main__':
    parse()
