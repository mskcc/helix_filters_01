#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the maf_filter.py script
"""
import sys
import os
import unittest
import csv
from tempfile import TemporaryDirectory, NamedTemporaryFile

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command, md5
    from .settings import DATA_SETS, BIN_DIR

if __name__ == "__main__":
    from tools import run_command, md5
    from settings import DATA_SETS, BIN_DIR

# need to import the module from the other dir
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from bin.cBioPortal_utils import parse_header_comments
sys.path.pop(0)


maf_filter_script = os.path.join(BIN_DIR, 'maf_filter.py')

class TestMafFilterScript(unittest.TestCase):
    def test_maf_filter_script1(self):
        """
        """
        input_maf_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'Sample1.Sample2.muts.maf')
        expected_analyst_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'analyst_file.txt') # 24
        expected_portal_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'portal_file.txt') # 19

        # input fixture has the correct number of lines
        with open(input_maf_file) as fin:
            input_maf_lines = len(fin.readlines())

        self.assertEqual(input_maf_lines, 12518)

        with TemporaryDirectory() as tmpdir:
            # bin/maf_filter.py Sample1.Sample2.muts.maf 2.x True analyst_file.txt portal_file.txt
            analyst_file = os.path.join(tmpdir, "analyst_file.txt")
            portal_file = os.path.join(tmpdir, "portal_file.txt")

            command = [ maf_filter_script, input_maf_file, "2.x", "True", analyst_file, portal_file ]

            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            with open(analyst_file) as fin:
                num_lines_analyst_file = len(fin.readlines())

            with open(portal_file) as fin:
                num_lines_portal_file = len(fin.readlines())

            self.assertEqual(num_lines_analyst_file, 24)
            self.assertEqual(num_lines_portal_file, 19)

            comments, start_line = parse_header_comments(portal_file)
            self.assertEqual(comments, ['# Versions: 2.x'])
            with open(portal_file) as fin:
                while start_line > 0:
                    next(fin)
                    start_line -= 1
                reader = csv.DictReader(fin, delimiter = '\t') # header_line = next(fin)
                portal_lines = [ row for row in reader ]

            self.assertEqual(len(portal_lines), 17)

            # get a subset of the lines' data for testing
            portal_mutations = []
            for row in portal_lines:
                t = ( row["Chromosome"], row["Start_Position"], row["End_Position"] )
                portal_mutations.append(t)

            # block of text copied from portal file; Chromosome	Start_Position	End_Position
            expected_contents = """8	56912099	56912099
X	123220555	123220555
11	69625447	69625447
17	78938112	78938113
12	102796343	102796343
6	117687313	117687313
8	141566089	141566089
10	70406514	70406514
X	76938716	76938716
6	117622265	117622265
5	1295250	1295250
5	176721774	176721774
12	57864555	57864555
19	11018780	11018782
5	176522632	176522632
8	69136857	69136857
7	2953083	2953083"""
            expected_contents = expected_contents.split('\n')
            expected_rows = []
            for item in expected_contents:
                Chromosome, Start_Position, End_Position = item.split('\t')
                t = ( Chromosome, Start_Position, End_Position )
                expected_rows.append(t)

            # make sure all the expected values are present
            self.assertEqual(set(portal_mutations), set(expected_rows))


            comments, start_line = parse_header_comments(analyst_file)
            self.assertEqual(comments, ['# Versions: 2.x'])
            with open(analyst_file) as fin:
                while start_line > 0:
                    next(fin)
                    start_line -= 1
                reader = csv.DictReader(fin, delimiter = '\t') # header_line = next(fin)
                analysis_lines = [ row for row in reader ]

            self.assertEqual(len(analysis_lines), 22)

            analysis_mutations = []
            for row in analysis_lines:
                t = ( row["Chromosome"], row["Start_Position"], row["End_Position"] )
                analysis_mutations.append(t)

            # block of text copied from analyst file; Chromosome	Start_Position	End_Position
            expected_contents = """11	69625447	69625447
8	69136857	69136857
8	141566089	141566089
X	76938716	76938716
12	49419992	49419992
X	123220555	123220555
5	176721774	176721774
19	11018780	11018782
5	176522632	176522632
8	56912099	56912099
17	78938112	78938113
12	57864555	57864555
6	117687313	117687313
10	70406514	70406514
3	142281434	142281434
5	1295250	1295250
6	117609901	117609901
12	102796343	102796343
6	117622265	117622265
12	121438953	121438953
7	2953083	2953083
2	212989483	212989483"""
            expected_contents = expected_contents.split('\n')
            expected_rows = []
            for item in expected_contents:
                Chromosome, Start_Position, End_Position = item.split('\t')
                t = ( Chromosome, Start_Position, End_Position )
                expected_rows.append(t)

            # make sure all the expected values are present
            self.assertEqual(set(analysis_mutations), set(expected_rows))




if __name__ == "__main__":
    unittest.main()
