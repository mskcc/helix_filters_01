#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
parity tests for the maf_filter.py script to ensure that expected mutations are output
"""
import sys
import os
import unittest
import csv
from tempfile import TemporaryDirectory

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command, load_mutations
    from .settings import MAF_FILTER_PARITY_DATA_DIR, BIN_DIR

if __name__ == "__main__":
    from tools import run_command, load_mutations
    from settings import MAF_FILTER_PARITY_DATA_DIR, BIN_DIR

# need to import the module from the other dir
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from bin.cBioPortal_utils import parse_header_comments
from bin import maf_filter
sys.path.pop(0)

maf_filter_script = os.path.join(BIN_DIR, 'maf_filter.py')

class TestMafFilterParity(unittest.TestCase):
    def test_maf_filter_parity1(self):
        """
        Test that the parity dataset gets filtered properly and the output matches the expected mutations
        """
        input_maf_file = os.path.join(MAF_FILTER_PARITY_DATA_DIR, 'all_samples.muts.maf')
        expected_analyst_file = os.path.join(MAF_FILTER_PARITY_DATA_DIR, 'analyst_file.txt')
        expected_portal_file = os.path.join(MAF_FILTER_PARITY_DATA_DIR, 'portal_file.txt')

        # sanity check; files have the correct number of rows
        comments, mutations = load_mutations(expected_portal_file)
        self.assertEqual(len(mutations), 1057)
        comments, mutations = load_mutations(expected_analyst_file)
        self.assertEqual(len(mutations), 1347)
        comments, mutations = load_mutations(input_maf_file, delete_cols = True) # try to reduce memory usage by deleting columns
        self.assertEqual(len(mutations), 4350504)

        # run the maf_filter script
        with TemporaryDirectory() as tmpdir:
            # bin/maf_filter.py Sample1.Sample2.muts.maf 2.x True analyst_file.txt portal_file.txt
            analyst_file = os.path.join(tmpdir, "analyst_file.txt")
            portal_file = os.path.join(tmpdir, "portal_file.txt")

            command = [ maf_filter_script, input_maf_file, "2.x", "True", analyst_file, portal_file ]
            print(">>> running script")

            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            with open(analyst_file) as fin:
                num_lines_analyst_file = len(fin.readlines())

            with open(portal_file) as fin:
                num_lines_portal_file = len(fin.readlines())

            self.assertEqual(num_lines_analyst_file, 27)
            self.assertEqual(num_lines_portal_file, 22)



if __name__ == "__main__":
    unittest.main()
