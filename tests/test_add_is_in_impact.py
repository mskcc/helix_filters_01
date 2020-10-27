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
        This test case handles the usage of an IMPACT list that lacks some chroms in the maf file
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
            comments, mutations = load_mutations(output_file)
            expected_mutations = [
                {'Chromosome': '1', 'Start_Position': '100', 'is_in_impact': 'True'},
                {'Chromosome': '2', 'Start_Position': '200', 'is_in_impact': 'False'},
                {'Chromosome': '3', 'Start_Position': '300', 'is_in_impact': 'False'},
                {'Chromosome': '4', 'Start_Position': '400', 'is_in_impact': 'False'}
                ]

            self.assertEqual(mutations, expected_mutations)

    def test_is_in_impact_1(self):
        """
        Test case with a larger IMPACT list that includes all chrom in the maf file
        """
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
                {'Chromosome': '1', 'Start_Position': '100', 'is_in_impact': 'True'},
                {'Chromosome': '2', 'Start_Position': '200', 'is_in_impact': 'False'},
                {'Chromosome': '3', 'Start_Position': '300', 'is_in_impact': 'False'}]

            self.assertEqual(mutations, expected_mutations)

    def test_is_in_impact_3(self):
        """
        Test IMPACT script with full size maf file
        """
        input_maf_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'Sample1.Sample2.muts.maf')
        impact_lines = [
            ['10', '100945885', '100945888'], # chrom, start, stop
            ['X', '9577377', '9577379'],
            ['9', '87476723', '87476725'],
        ]
        with TemporaryDirectory() as tmpdir:
            output_file = os.path.join(tmpdir, "output.txt")
            impact_file = write_table(tmpdir = tmpdir, filename = 'IMPACT.txt', lines = impact_lines)
            command = [ impact_script, '--input_file', input_maf_file, '--output_file', output_file, '--IMPACT_file', impact_file ]
            returncode, proc_stdout, proc_stderr = run_command(command, testcase = self, validate = True)

            # validate output mutations
            comments, mutations = load_mutations(output_file)
            self.assertEqual(len(mutations), 12514)
            num_True = 0
            num_False = 0
            for mut in mutations:
                if mut['is_in_impact'] == 'True':
                    num_True += 1
                elif mut['is_in_impact'] == 'False':
                    num_False += 1
            self.assertEqual(num_True, 3)
            self.assertEqual(num_False, 12511)


# run the test suite from the command line
if __name__ == "__main__":
    unittest.main()
