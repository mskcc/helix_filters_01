#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the concat-tables.py script
"""
import sys
import os
import unittest
import csv
import importlib
from pathlib import Path

# need to import the module from the other dir
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from pluto.tools import PlutoTestCase
from settings import BIN_DIR
concat_tables = importlib.import_module("bin.concat-tables")
sys.path.pop(0)

concat_tables_script = os.path.join(BIN_DIR, 'concat-tables.py')

class TestConcatTables(PlutoTestCase):
    def test_find_start_line(self):
        """
        Test that the script correctly finds the starting line for the header
        when a file has comments
        """
        lines1 = [
        '# comment 1\n'
        'HEADER1\tHEADER2\n'
        'foo1\tbar1\n'
        ]
        lines2 = [
        '# comment 2\n',
        '# comment 3\n',
        'HEADER1\tHEADER3\n'
        'foo2\tbaz2\n'
        ]
        lines3 = [
        'HEADER1\tHEADER3\n'
        'foo2\tbaz2\n'
        ]
        input_file1 = os.path.join(self.tmpdir, "input1.txt")
        input_file2 = os.path.join(self.tmpdir, "input2.txt")
        input_file3 = os.path.join(self.tmpdir, "input3.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)
        with open(input_file3, "w") as fout:
            fout.writelines(lines3)

        start_line = concat_tables.find_start_line(input_file1)
        self.assertEqual(start_line, 1)

        start_line = concat_tables.find_start_line(input_file2)
        self.assertEqual(start_line, 2)

        start_line = concat_tables.find_start_line(input_file3)
        self.assertEqual(start_line, 0)

    def test_get_all_fieldnames1(self):
        """
        Test that the fieldname retrieval function works correctly
        """
        lines1 = [
        'HEADER1\tHEADER2\n',
        'foo1\tbar1\n'
        ]
        lines2 = [
        'HEADER1\tHEADER3\n',
        'foo2\tbaz2\n'
        ]
        input_file1 = os.path.join(self.tmpdir, "input1.txt")
        input_file2 = os.path.join(self.tmpdir, "input2.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)

        fieldnames = concat_tables.get_all_fieldnames([input_file1, input_file2], delimiter = '\t')
        self.assertEqual([f for f in fieldnames], ['HEADER1', 'HEADER2', 'HEADER3'])

    def test_get_all_fieldnames_with_comments(self):
        """
        Test that the correct fieldnames are returned when mixed files with comments are provided
        """
        lines1 = [
        '# comment 1\n',
        'HEADER1\tHEADER2\n',
        'foo1\tbar1\n'
        ]
        lines2 = [
        '# comment 2\n',
        'HEADER1\tHEADER3\n',
        'foo2\tbaz2\n'
        ]
        input_file1 = os.path.join(self.tmpdir, "input1.txt")
        input_file2 = os.path.join(self.tmpdir, "input2.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)
        fieldnames = concat_tables.get_all_fieldnames([input_file1, input_file2], delimiter = '\t', has_comments = True, comment_char = '#')
        self.assertEqual([f for f in fieldnames], ['HEADER1', 'HEADER2', 'HEADER3'])

    def test_get_all_fieldnames_with_mixed_comments(self):
        """
        Test that the correct fieldnames are returned when mixed files with and without comments are provided
        """
        lines1 = [
        '# comment 1\n',
        'HEADER1\tHEADER2\n',
        'foo1\tbar1\n'
        ]
        lines2 = [
        'HEADER1\tHEADER3\n',
        'foo2\tbaz2\n'
        ]
        input_file1 = os.path.join(self.tmpdir, "input1.txt")
        input_file2 = os.path.join(self.tmpdir, "input2.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)
        fieldnames = concat_tables.get_all_fieldnames([input_file1, input_file2], delimiter = '\t', has_comments = True, comment_char = '#')
        self.assertEqual([f for f in fieldnames], ['HEADER1', 'HEADER2', 'HEADER3'])

    def test_get_all_comments1(self):
        """
        Test that all the comments from the input files are retrieved properly
        """
        lines1 = [
        '# comment 1\n'
        'HEADER1\tHEADER2\n'
        'foo1\tbar1\n'
        ]
        lines2 = [
        '# comment 2\n'
        '# comment 3\n'
        'HEADER1\tHEADER3\n'
        'foo2\tbaz2\n'
        ]
        input_file1 = os.path.join(self.tmpdir, "input1.txt")
        input_file2 = os.path.join(self.tmpdir, "input2.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)
        comments = concat_tables.get_all_comments([input_file1, input_file2], comment_char = '#')
        expected_comments = [
        '# comment 1',
        '# comment 2',
        '# comment 3'
        ]
        self.assertEqual(comments, expected_comments)

    def test_concat_tables1(self):
        """
        Test that the script runs as expected with a single input file
        """
        lines1 = [
        'HEADER1\tHEADER2\n'
        'foo1\tbar1\n'
        ]
        input_file = os.path.join(self.tmpdir, "input.txt")
        output_file = os.path.join(self.tmpdir, "output.txt")
        with open(input_file, "w") as fout:
            fout.writelines(lines1)

        command = [ concat_tables_script, input_file, '-o', output_file ]

        returncode, proc_stdout, proc_stderr = self.run_command(command)

        if returncode != 0:
            print(proc_stderr)

        self.assertEqual(returncode, 0)

        with open(output_file) as fin:
            lines = fin.readlines()

        expected_lines = ['HEADER1\tHEADER2\n', 'foo1\tbar1\n']

        self.assertEqual(lines, expected_lines)

    def test_concat_tables2(self):
        """
        test the script with multiple input files with the same headers
        """
        lines1 = [
        'HEADER1\tHEADER2\n'
        'foo1\tbar1\n'
        ]
        lines2 = [
        'HEADER1\tHEADER2\n'
        'foo2\tbar2\n'
        ]
        input_file1 = os.path.join(self.tmpdir, "input1.txt")
        input_file2 = os.path.join(self.tmpdir, "input2.txt")
        output_file = os.path.join(self.tmpdir, "output.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)

        command = [ concat_tables_script, '-o', output_file, input_file1, input_file2 ]

        returncode, proc_stdout, proc_stderr = self.run_command(command)

        if returncode != 0:
            print(proc_stderr)

        self.assertEqual(returncode, 0)

        with open(output_file) as fin:
            lines = fin.readlines()

        expected_lines = [
        'HEADER1\tHEADER2\n',
        'foo1\tbar1\n',
        'foo2\tbar2\n'
        ]

        self.assertEqual(lines, expected_lines)

    def test_concat_tables_diff_header(self):
        """
        test the script with multiple input files with different headers
        """
        lines1 = [
        'HEADER1\tHEADER2\n'
        'foo1\tbar1\n'
        ]
        lines2 = [
        'HEADER1\tHEADER3\n'
        'foo2\tbaz2\n'
        ]
        input_file1 = os.path.join(self.tmpdir, "input1.txt")
        input_file2 = os.path.join(self.tmpdir, "input2.txt")
        output_file = os.path.join(self.tmpdir, "output.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)

        command = [ concat_tables_script, '-o', output_file, input_file1, input_file2 ]

        returncode, proc_stdout, proc_stderr = self.run_command(command)

        if returncode != 0:
            print(proc_stderr)

        self.assertEqual(returncode, 0)

        with open(output_file) as fin:
            lines = fin.readlines()

        expected_lines = [
        'HEADER1\tHEADER2\tHEADER3\n',
        'foo1\tbar1\t.\n',
        'foo2\t.\tbaz2\n'
        ]

        self.assertEqual(lines, expected_lines)

    def test_concat_tables_na_str(self):
        """
        test the script with multiple input files with different headers and a custom NA value
        """
        lines1 = [
        'HEADER1\tHEADER2\n'
        'foo1\tbar1\n'
        ]
        lines2 = [
        'HEADER1\tHEADER3\n'
        'foo2\tbaz2\n'
        ]
        input_file1 = os.path.join(self.tmpdir, "input1.txt")
        input_file2 = os.path.join(self.tmpdir, "input2.txt")
        output_file = os.path.join(self.tmpdir, "output.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)

        command = [ concat_tables_script, '-o', output_file, '-n', 'NA', input_file1, input_file2 ]

        returncode, proc_stdout, proc_stderr = self.run_command(command)

        if returncode != 0:
            print(proc_stderr)

        self.assertEqual(returncode, 0)

        with open(output_file) as fin:
            lines = fin.readlines()

        expected_lines = [
        'HEADER1\tHEADER2\tHEADER3\n',
        'foo1\tbar1\tNA\n',
        'foo2\tNA\tbaz2\n'
        ]

        self.assertEqual(lines, expected_lines)

    def test_concat_tables_with_comments_no_arg(self):
        """
        Test that the script breaks if you try to concat tables that have comment lines but do not specify '--comments'
        """
        lines1 = [
        '# comment\n',
        'HEADER1\tHEADER2\n',
        'foo1\tbar1\n'
        ]
        lines2 = [
        'HEADER1\tHEADER3\n',
        'foo2\tbaz2\n'
        ]
        input_file1 = os.path.join(self.tmpdir, "input1.txt")
        input_file2 = os.path.join(self.tmpdir, "input2.txt")
        output_file = os.path.join(self.tmpdir, "output.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)

        command = [ concat_tables_script, '-o', output_file, input_file1, input_file2 ]
        # should break
        returncode, proc_stdout, proc_stderr = self.run_command(command)
        self.assertTrue(returncode > 0)

    def test_concat_tables_with_comments1(self):
        """
        Test that you can concat tables if they have comment lines when you specify the extra cli arg
        """
        lines1 = [
        '# comment\n',
        'HEADER1\tHEADER2\n',
        'foo1\tbar1\n'
        ]
        lines2 = [
        'HEADER1\tHEADER3\n',
        'foo2\tbaz2\n'
        ]
        input_file1 = os.path.join(self.tmpdir, "input1.txt")
        input_file2 = os.path.join(self.tmpdir, "input2.txt")
        output_file = os.path.join(self.tmpdir, "output.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)

        command = [ concat_tables_script, '--comments', '-o', output_file, input_file1, input_file2 ]

        returncode, proc_stdout, proc_stderr = self.run_command(command)

        if returncode != 0:
            print(proc_stderr)

        self.assertEqual(returncode, 0)

        with open(output_file) as fin:
            lines = fin.readlines()

        expected_lines = [
        '# comment\n',
        'HEADER1\tHEADER2\tHEADER3\n',
        'foo1\tbar1\t.\n',
        'foo2\t.\tbaz2\n'
        ]

        self.assertEqual(lines, expected_lines)

    def test_concat_tables_with_comments2(self):
        """
        Test that you can concat tables if they have comment lines when you specify the extra cli arg
        """
        lines1 = [
        '# comment 1\n',
        'HEADER1\tHEADER2\n',
        'foo1\tbar1\n'
        ]
        lines2 = [
        '# comment 2\n',
        'HEADER1\tHEADER3\n',
        'foo2\tbaz2\n'
        ]
        lines3 = [
        '# comment 1\n',
        '# comment 3\n',
        'HEADER1\tHEADER3\n',
        'foo3\tbaz3\n'
        ]
        input_file1 = os.path.join(self.tmpdir, "input1.txt")
        input_file2 = os.path.join(self.tmpdir, "input2.txt")
        input_file3 = os.path.join(self.tmpdir, "input3.txt")
        output_file = os.path.join(self.tmpdir, "output.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)
        with open(input_file3, "w") as fout:
            fout.writelines(lines3)

        command = [ concat_tables_script, '--comments', '-o', output_file, input_file1, input_file2, input_file3 ]

        returncode, proc_stdout, proc_stderr = self.run_command(command)

        if returncode != 0:
            print(proc_stderr)

        self.assertEqual(returncode, 0)

        with open(output_file) as fin:
            lines = fin.readlines()

        expected_lines = [
        '# comment 1\n',
        '# comment 2\n',
        '# comment 3\n',
        'HEADER1\tHEADER2\tHEADER3\n',
        'foo1\tbar1\t.\n',
        'foo2\t.\tbaz2\n',
        'foo3\t.\tbaz3\n'
        ]

        self.assertEqual(lines, expected_lines)

    def test_concat_files_from_dir(self):
        """
        Test case for using concat-tables script with an input of directory of files
        """
        input_dir = os.path.join(self.tmpdir, "input")
        Path(input_dir).mkdir(parents=True, exist_ok=True)
        lines1 = [
        '# comment 1\n',
        'HEADER1\tHEADER2\n',
        'foo1\tbar1\n'
        ]
        lines2 = [
        '# comment 2\n',
        'HEADER1\tHEADER3\n',
        'foo2\tbaz2\n'
        ]
        lines3 = [
        '# comment 1\n',
        '# comment 3\n',
        'HEADER1\tHEADER3\n',
        'foo3\tbaz3\n'
        ]
        input_file1 = os.path.join(input_dir, "input1.txt")
        input_file2 = os.path.join(input_dir, "input2.txt")
        input_file3 = os.path.join(input_dir, "input3.txt")
        output_file = os.path.join(self.tmpdir, "output.txt")
        with open(input_file1, "w") as fout:
            fout.writelines(lines1)
        with open(input_file2, "w") as fout:
            fout.writelines(lines2)
        with open(input_file3, "w") as fout:
            fout.writelines(lines3)

        command = [ concat_tables_script, '--dir', '--comments', '-o', output_file, input_dir ]

        returncode, proc_stdout, proc_stderr = self.run_command(command, testcase = self, validate = True)

        with open(output_file) as fin:
            lines = fin.readlines()

        expected_lines = [
        '# comment 1\n',
        '# comment 2\n',
        '# comment 3\n',
        'HEADER1\tHEADER2\tHEADER3\n',
        'foo1\tbar1\t.\n',
        'foo2\t.\tbaz2\n',
        'foo3\t.\tbaz3\n'
        ]

        self.assertEqual(lines, expected_lines)


if __name__ == "__main__":
    unittest.main()
