#!/usr/bin/env python3
"""
unit tests for the add_is_in_impact.py script
"""
import os
import unittest
from tempfile import TemporaryDirectory

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command, load_mutations, write_table
    from .settings import DATA_SETS, BIN_DIR

if __name__ == "__main__":
    from tools import run_command, load_mutations, write_table
    from settings import DATA_SETS, BIN_DIR

impact_script = os.path.join(BIN_DIR, 'add_is_in_impact.py')

class TestInImpactScript(unittest.TestCase):
    def test_is_in_impact_0(self):
        """
        Test that maf entries are flagged if they are in the IMPACT set
        """
        maf_lines = [
            ['Chromosome', 'Start_Position'],
            ['1', '100'],
            ['2', '200'],
            ['3', '300'],
            ['4', '400']
        ]
        impact_lines = [
            ['1', '50', '150'] # chrom, start, stop
        ]

        # run the script in a temporary directory
        with TemporaryDirectory() as tmpdir:
            input_maf_file = write_table(tmpdir = tmpdir, filename = 'input.maf', lines = maf_lines)
            impact_file = write_table(tmpdir = tmpdir, filename = 'IMPACT.txt', lines = impact_lines)
            output_file = os.path.join(tmpdir, "output.txt")

            # command line arguments to run script
            command = [ impact_script, '--input_file', input_maf_file, '--output_file', output_file, '--IMPACT_file', impact_file ]
            returncode, proc_stdout, proc_stderr = run_command(command, testcase = self, validate = True)

            # TODO: get this test case to work and validate output

    def test_is_in_impact_1(self):
        maf_lines = [
            ['Chromosome', 'Start_Position'],
            ['1', '100'],
            ['2', '200'],
            ['3', '300']
        ]
        impact_lines = [
            ['1', '50', '150'], # chrom, start, stop
            ['2', '50', '150'],
            ['3', '50', '150'],
        ]
        with TemporaryDirectory() as tmpdir:
            input_maf_file = write_table(tmpdir = tmpdir, filename = 'input.maf', lines = maf_lines)
            impact_file = write_table(tmpdir = tmpdir, filename = 'IMPACT.txt', lines = impact_lines)
            output_file = os.path.join(tmpdir, "output.txt")

            # command line arguments to run script
            command = [ impact_script, '--input_file', input_maf_file, '--output_file', output_file, '--IMPACT_file', impact_file ]
            returncode, proc_stdout, proc_stderr = run_command(command, testcase = self, validate = True)

            comments, mutations = load_mutations(output_file)
            expected_mutations = [
                {'Chromosome': '1', 'Start_Position': '100', 'Is_in_IMPACT': 'True'},
                {'Chromosome': '2', 'Start_Position': '200', 'Is_in_IMPACT': 'False'},
                {'Chromosome': '3', 'Start_Position': '300', 'Is_in_IMPACT': 'False'}]

            self.assertEqual(mutations, expected_mutations)


# run the test suite from the command line
if __name__ == "__main__":
    unittest.main()
