#!/usr/bin/env python3
"""
unit tests for the add_af.py script
"""
import os
import unittest
from tempfile import TemporaryDirectory

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command, load_mutations, write_table
    from .settings import BIN_DIR # DATA_SETS

if __name__ == "__main__":
    from tools import run_command, load_mutations, write_table
    from settings import BIN_DIR # DATA_SETS

test_script = os.path.join(BIN_DIR, 'add_af.py')

class TestAddAf(unittest.TestCase):
    def test_add_af_1(self):
        """
        test case for adding the tumor variant allele frequency column to a maf file
        """
        maf_lines = [
            ['# comment 1'],
            ['# comment 2'],
            ['Hugo_Symbol', 't_depth', 't_alt_count'],
            ['SUFU', '100', '75'],
            ['GOT1', '100', '1'],
            ['SOX9', '100', '0'],
        ]
        with TemporaryDirectory() as tmpdir:
            input_maf_file = write_table(tmpdir = tmpdir, filename = 'input.maf', lines = maf_lines)
            output_file = os.path.join(tmpdir, "output.maf")

            # command line arguments to run script
            command = [ test_script, input_maf_file, output_file ]
            returncode, proc_stdout, proc_stderr = run_command(command, testcase = self, validate = True)

            # parse the output
            comments, mutations = load_mutations(output_file)

            expected_comments = ['# comment 1', '# comment 2']
            self.assertEqual(comments, expected_comments)

            expected_mutations = [
                {'Hugo_Symbol': 'SUFU', 't_depth': '100', 't_alt_count':'75', 't_af': '0.75'},
                {'Hugo_Symbol': 'GOT1', 't_depth': '100', 't_alt_count':'1', 't_af': '0.01'},
                {'Hugo_Symbol': 'SOX9', 't_depth': '100', 't_alt_count':'0', 't_af': '0.0'}
                ]
            self.assertEqual(mutations, expected_mutations)

if __name__ == "__main__":
    unittest.main()
