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
    from .settings import DATA_SETS, BIN_DIR, TARGETS

if __name__ == "__main__":
    from tools import run_command, load_mutations, write_table
    from settings import DATA_SETS, BIN_DIR, TARGETS

impact_script = os.path.join(BIN_DIR, 'add_is_in_impact.py')

class TestInImpactScript(unittest.TestCase):
    def test_is_in_impact_0(self):
        """
        Test that maf entries are flagged if they are in the IMPACT set
        Use tiny dummy maf and IMPACT gene list files
        """
        maf_lines = [
            ['Hugo_Symbol'],
            ['SUFU'],
            ['GOT1']
        ]
        impact_lines = [
            ['SUFU'],
            ['TP53']
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
                {'Hugo_Symbol': 'SUFU', 'is_in_impact': 'True'},
                {'Hugo_Symbol': 'GOT1', 'is_in_impact': 'False'}
                ]

            self.assertEqual(mutations, expected_mutations)


    def test_is_in_impact_1(self):
        """
        Test that maf entries are flagged if they are in the IMPACT set
        Use tiny dummy maf and IMPACT gene list files
        """
        maf_lines = [
            ['Hugo_Symbol'],
            ['SUFU'],
            ['GOT1'],
            ['EGFR'],
            ['SOX9'],
        ]
        impact_lines = [
            ['SUFU'],
            ['SOX9']
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
                {'Hugo_Symbol': 'SUFU', 'is_in_impact': 'True'},
                {'Hugo_Symbol': 'GOT1', 'is_in_impact': 'False'},
                {'Hugo_Symbol': 'EGFR', 'is_in_impact': 'False'},
                {'Hugo_Symbol': 'SOX9', 'is_in_impact': 'True'}
                ]

            self.assertEqual(mutations, expected_mutations)

    def test_is_in_impact_full_maf(self):
       """
       Test IMPACT script with full size maf file
       """
       input_maf_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'Sample1.Sample2.muts.maf')
       impact_lines = [
           ['SUFU'],
           ['TP53']
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
           self.assertEqual(num_True, 56)
           self.assertEqual(num_False, 12458)

    def test_is_in_impact_assay_labels(self):
        """
        Test case for including assay labels in the IMPACT gene list file
        """
        self.maxDiff = None
        impact_lines = [
            ['SUFU', 'IMPACT468'], # same gene, multiple assays
            ['SUFU', 'IMPACT505'],
            ['TP53', 'IMPACT505'],
            ['TP53', 'IMPACT468'],
            ['SOX9', 'IMPACT468'], # only one assay
        ]
        maf_lines = [
            ['Hugo_Symbol'],
            ['SUFU'],
            ['GOT1'], # not in the IMPACT list
            ['EGFR'],  # not in the IMPACT list
            ['TP53'],
            ['SOX9'],
        ]
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
                {'Hugo_Symbol': 'SUFU', 'is_in_impact': 'True'},
                {'Hugo_Symbol': 'GOT1', 'is_in_impact': 'False'},
                {'Hugo_Symbol': 'EGFR', 'is_in_impact': 'False'},
                {'Hugo_Symbol': 'TP53', 'is_in_impact': 'True'},
                {'Hugo_Symbol': 'SOX9', 'is_in_impact': 'True'}
                ]

            self.assertEqual(mutations, expected_mutations)

# TODO: restore this test case once we have the actual IMPACT gene list file
#    def test_is_in_impact_with_targets(self):
#        """
#        Test IMPACT script with full size maf file and real targets file
#        """
#        input_maf_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'Sample1.Sample2.muts.maf')
#        impact_file = TARGETS['IMPACT468_b37']['targets_list']
#        with TemporaryDirectory() as tmpdir:
#            output_file = os.path.join(tmpdir, "output.txt")
#            command = [ impact_script, '--input_file', input_maf_file, '--output_file', output_file, '--IMPACT_file', impact_file ]
#            returncode, proc_stdout, proc_stderr = run_command(command, testcase = self, validate = True)
#
#            # validate output mutations
#            comments, mutations = load_mutations(output_file)
#            self.assertEqual(len(mutations), 12514)
#            num_True = 0
#            num_False = 0
#            for mut in mutations:
#                if mut['is_in_impact'] == 'True':
#                    num_True += 1
#                elif mut['is_in_impact'] == 'False':
#                    num_False += 1
#            self.assertEqual(num_True, 6160)
#            self.assertEqual(num_False, 6354)


# run the test suite from the command line
if __name__ == "__main__":
    unittest.main()
