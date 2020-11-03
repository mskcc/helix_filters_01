#!/usr/bin/env python3
"""
Tests for maf col filter script
"""
import os
import sys
import unittest
from tempfile import TemporaryDirectory

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command, load_mutations, write_table
    from .settings import DATA_SETS, BIN_DIR, TARGETS

if __name__ == "__main__":
    from tools import run_command, load_mutations, write_table
    from settings import DATA_SETS, BIN_DIR, TARGETS

# need to import the module from the other dir
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from bin import maf_col_filter
sys.path.pop(0)

test_script = os.path.join(BIN_DIR, 'maf_col_filter.py')

class TestMafColFilterScript(unittest.TestCase):
    def test_maf_col_filter_0(self):
        """
        Test maf col filter with tiny dummy dataset
        """
        maf_lines = [
            ['# comment 1'], # keep the comments
            ['# comment 2'],
            ['Hugo_Symbol', 'foo_value'], # foo_value column should be removed in output
            ['SUFU', '1'],
            ['GOT1', '2']
        ]

        # run the script in a temporary directory
        with TemporaryDirectory() as tmpdir:
            input_maf_file = write_table(tmpdir = tmpdir, filename = 'input.maf', lines = maf_lines)
            output_file = os.path.join(tmpdir, "output.txt")

            # command line arguments to run script
            command = [ test_script, input_maf_file, output_file ]
            returncode, proc_stdout, proc_stderr = run_command(command, testcase = self, validate = True)

            comments, mutations = load_mutations(output_file)

            expected_comments = ['# comment 1', '# comment 2']
            self.assertEqual(comments, expected_comments)

            expected_mutations = [
                {'Hugo_Symbol': 'SUFU'},
                {'Hugo_Symbol': 'GOT1'}
                ]

            self.assertEqual(mutations, expected_mutations)

    def test_maf_col_filter_1(self):
        """
        Test maf col filter with extra columns that need to be kept
        """
        self.maxDiff = None
        maf_lines = [
            ['# comment 1'],
            ['# comment 2'],
            ['Hugo_Symbol', 't_depth', 't_alt_count', 't_af', 'is_in_impact', 'impact_assays', 'foo_value'],
            ['SUFU', '100', '75', '0.75', 'True', '.', 'foo'],
            ['GOT1', '100', '1', '0.01', 'False', '.', 'bar'],
            ['SOX9', '100', '0', '0.0', 'True', '.', 'baz'],
        ]

        # run the script in a temporary directory
        with TemporaryDirectory() as tmpdir:
            input_maf_file = write_table(tmpdir = tmpdir, filename = 'input.maf', lines = maf_lines)
            output_file = os.path.join(tmpdir, "output.txt")

            # command line arguments to run script
            command = [ test_script, input_maf_file, output_file ]
            returncode, proc_stdout, proc_stderr = run_command(command, testcase = self, validate = True)

            comments, mutations = load_mutations(output_file)

            expected_comments = ['# comment 1', '# comment 2']
            self.assertEqual(comments, expected_comments)

            expected_mutations = [
                {'Hugo_Symbol': 'SUFU', 't_depth': '100', 't_alt_count':'75', 't_af': '0.75', 'is_in_impact': 'True', 'impact_assays': '.'},
                {'Hugo_Symbol': 'GOT1', 't_depth': '100', 't_alt_count':'1', 't_af': '0.01', 'is_in_impact': 'False', 'impact_assays': '.'},
                {'Hugo_Symbol': 'SOX9', 't_depth': '100', 't_alt_count':'0', 't_af': '0.0', 'is_in_impact': 'True', 'impact_assays': '.'}
                ]
            self.assertEqual(mutations, expected_mutations)


    def test_maf_col_filter_full(self):
        """
        Test the col filter with a full sized dataset
        """
        input_maf_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'Sample1.Sample2.muts.maf')

        with TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "output.txt")
            command = [ test_script, input_maf_file, output_file ]
            returncode, proc_stdout, proc_stderr = run_command(command, testcase = self, validate = True)

            # validate output mutations
            comments, mutations = load_mutations(output_file)
            self.assertEqual(len(mutations), 12514)

            for key in mutations[0].keys():
                self.assertTrue(key in maf_col_filter.cols_to_keep)

            self.assertTrue( len(mutations[0].keys()) <= len(maf_col_filter.cols_to_keep) )

# run the test suite from the command line
if __name__ == "__main__":
    unittest.main()
