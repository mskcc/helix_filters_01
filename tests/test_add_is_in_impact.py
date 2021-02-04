#!/usr/bin/env python3
"""
unit tests for the add_is_in_impact.py script
"""
import sys
import os
import unittest

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from pluto.tools import PlutoTestCase
from pluto.settings import DATA_SETS
from settings import BIN_DIR, IMPACT_GENE_LIST
sys.path.pop(0)

impact_script = os.path.join(BIN_DIR, 'add_is_in_impact.py')

class TestInImpactScript(PlutoTestCase):
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
        input_maf_file = self.write_table(tmpdir = self.tmpdir, filename = 'input.maf', lines = maf_lines)
        impact_file = self.write_table(tmpdir = self.tmpdir, filename = 'IMPACT.txt', lines = impact_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")

        # command line arguments to run script
        command = [ impact_script, '--input_file', input_maf_file, '--output_file', output_file, '--IMPACT_file', impact_file ]
        returncode, proc_stdout, proc_stderr = self.run_command(command, testcase = self, validate = True)

        comments, mutations = self.load_mutations(output_file)
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
        input_maf_file = self.write_table(tmpdir = self.tmpdir, filename = 'input.maf', lines = maf_lines)
        impact_file = self.write_table(tmpdir = self.tmpdir, filename = 'IMPACT.txt', lines = impact_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")

        # command line arguments to run script
        command = [ impact_script, '--input_file', input_maf_file, '--output_file', output_file, '--IMPACT_file', impact_file ]
        returncode, proc_stdout, proc_stderr = self.run_command(command, testcase = self, validate = True)

        comments, mutations = self.load_mutations(output_file)
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
       output_file = os.path.join(self.tmpdir, "output.txt")
       impact_file = self.write_table(tmpdir = self.tmpdir, filename = 'IMPACT.txt', lines = impact_lines)
       command = [ impact_script, '--input_file', input_maf_file, '--output_file', output_file, '--IMPACT_file', impact_file ]
       returncode, proc_stdout, proc_stderr = self.run_command(command, testcase = self, validate = True)

       # validate output mutations
       comments, mutations = self.load_mutations(output_file)
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
        input_maf_file = self.write_table(tmpdir = self.tmpdir, filename = 'input.maf', lines = maf_lines)
        impact_file = self.write_table(tmpdir = self.tmpdir, filename = 'IMPACT.txt', lines = impact_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")

        # command line arguments to run script
        command = [ impact_script, '--input_file', input_maf_file, '--output_file', output_file, '--IMPACT_file', impact_file ]
        returncode, proc_stdout, proc_stderr = self.run_command(command, testcase = self, validate = True)

        comments, mutations = self.load_mutations(output_file)
        expected_mutations = [
            {'Hugo_Symbol': 'SUFU', 'is_in_impact': 'True'},
            {'Hugo_Symbol': 'GOT1', 'is_in_impact': 'False'},
            {'Hugo_Symbol': 'EGFR', 'is_in_impact': 'False'},
            {'Hugo_Symbol': 'TP53', 'is_in_impact': 'True'},
            {'Hugo_Symbol': 'SOX9', 'is_in_impact': 'True'}
            ]

        self.assertEqual(mutations, expected_mutations)

    def test_is_in_impact_assay_labels_in_output(self):
        """
        Test case for including assay labels in the IMPACT gene list file
        Also include the assay labels in the output
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
        input_maf_file = self.write_table(tmpdir = self.tmpdir, filename = 'input.maf', lines = maf_lines)
        impact_file = self.write_table(tmpdir = self.tmpdir, filename = 'IMPACT.txt', lines = impact_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")

        # command line arguments to run script
        command = [ impact_script, '--input_file', input_maf_file, '--output_file', output_file, '--IMPACT_file', impact_file, '--include-assay' ]
        returncode, proc_stdout, proc_stderr = self.run_command(command, testcase = self, validate = True)

        comments, mutations = self.load_mutations(output_file)
        expected_mutations = [
            {'Hugo_Symbol': 'SUFU', 'is_in_impact': 'True', 'impact_assays': 'IMPACT468,IMPACT505'},
            {'Hugo_Symbol': 'GOT1', 'is_in_impact': 'False', 'impact_assays': '.'},
            {'Hugo_Symbol': 'EGFR', 'is_in_impact': 'False', 'impact_assays': '.'},
            {'Hugo_Symbol': 'TP53', 'is_in_impact': 'True', 'impact_assays': 'IMPACT468,IMPACT505'},
            {'Hugo_Symbol': 'SOX9', 'is_in_impact': 'True', 'impact_assays': 'IMPACT468'}
            ]

        self.assertEqual(mutations, expected_mutations)

    def test_is_in_impact_with_targets(self):
        """
        Test IMPACT script with full size maf file and real targets file
        """
        self.maxDiff = None
        input_maf_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'Sample1.Sample2.muts.maf')
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [ impact_script, '--input_file', input_maf_file, '--output_file', output_file, '--IMPACT_file', IMPACT_GENE_LIST, '--include-assay' ]
        returncode, proc_stdout, proc_stderr = self.run_command(command, testcase = self, validate = True)

        # validate output mutations
        comments, mutations = self.load_mutations(output_file)
        self.assertEqual(len(mutations), 12514)
        num_True = 0
        num_False = 0
        assay_counts = {
        '.': 0,
        'IMPACT341,IMPACT410': 0,
        'IMPACT341,IMPACT410,IMPACT468,IMPACT505': 0,
        'IMPACT410,IMPACT468,IMPACT505': 0,
        'IMPACT468,IMPACT505': 0,
        'IMPACT505': 0
        }
        for mut in mutations:
            assay_counts[mut['impact_assays']] += 1
            if mut['is_in_impact'] == 'True':
                num_True += 1
            elif mut['is_in_impact'] == 'False':
                num_False += 1

        self.assertEqual(num_True, 8367)
        self.assertEqual(num_False, 4147)

        expected_assay_counts = {
        '.': 4147,
        'IMPACT341,IMPACT410': 19,
        'IMPACT341,IMPACT410,IMPACT468,IMPACT505': 6222,
        'IMPACT410,IMPACT468,IMPACT505': 819,
        'IMPACT468,IMPACT505': 1045,
        'IMPACT505': 262
        }

        self.assertDictEqual(assay_counts, expected_assay_counts)

# run the test suite from the command line
if __name__ == "__main__":
    unittest.main()
