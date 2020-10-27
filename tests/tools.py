"""
Helper functions for running tests
"""
import os
import subprocess as sp
import hashlib
import csv

def run_command(args, testcase = None, validate = False):
    """
    Helper function to run a shell command easier

    Parameters
    ----------
    args: list
        a list of shell args to execute
    validate: bool
        whether to check that the exit code was 0; requires `testcase`
    testcase: unittest.TestCase
        a test case instance for making assertions
    """
    process = sp.Popen(args, stdout = sp.PIPE, stderr = sp.PIPE, universal_newlines = True)
    proc_stdout, proc_stderr = process.communicate()
    returncode = process.returncode
    proc_stdout = proc_stdout.strip()
    proc_stderr = proc_stderr.strip()

    # check that it ran successfully; requires testcase to be passed !
    if validate:
        if returncode != 0:
            print(proc_stderr)
        testcase.assertEqual(returncode, 0)
    return(returncode, proc_stdout, proc_stderr)

def md5(filename):
    """
    Generate md5sum hash of a file
    https://stackoverflow.com/questions/3431825/generating-an-md5-checksum-of-a-file
    """
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def parse_header_comments(filename):
    """
    Parse a file with comments in its header to return the comments and the line number to start reader from

    comments, start_line = parse_header_comments(filename)
    with open(portal_file) as fin:
        while start_line > 0:
            next(fin)
            start_line -= 1
        reader = csv.DictReader(fin, delimiter = '\t') # header_line = next(fin)
        portal_lines = [ row for row in reader ]
    """
    comments = []
    start_line = 0
    # find the first line without comments
    with open(filename) as fin:
        for i, line in enumerate(fin):
            if line.startswith('#'):
                comments.append(line.strip())
                start_line += 1
    return(comments, start_line)

def load_mutations(filename, keep_cols = None, delete_cols = False):
    """
    Load the mutations from a file to use for testing
    """
    comments, start_line = parse_header_comments(filename)
    with open(filename) as fin:
        while start_line > 0:
            next(fin)
            start_line -= 1
        reader = csv.DictReader(fin, delimiter = '\t')
        # filter columns if they were passed
        if keep_cols:
            mutations = []
            for row in reader:
                d = {}
                for key in keep_cols:
                    d[key] = row[key]
                mutations.append(d)
                del row # remove immediately to save memory
        # delete all columns to save memory on large datasets when we dont  actually need the mutation data
        elif delete_cols:
            mutations = []
            for row in reader:
                row.clear()
                mutations.append(row)
        else:
            mutations = [ row for row in reader ]
    return(comments, mutations)

def write_table(tmpdir, filename, lines, delimiter = '\t'):
    """
    Write a table to a temp location
    """
    filepath = os.path.join(tmpdir, filename)
    with open(filepath, "w") as f:
        for line in lines:
            line_str = delimiter.join(line) + '\n'
            f.write(line_str)
    return(filepath)
