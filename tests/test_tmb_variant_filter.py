#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cases for filtering variants for calculating TMB tumor mutational burden
"""
import os
import sys
import unittest
from tools import TmpDirTestCase, run_command, write_table, load_mutations, dicts2lines
from settings import BIN_DIR

script = os.path.join(BIN_DIR, 'tmb_variant_filter.py')

class TestTMBVariantFilter(TmpDirTestCase):
    def test_tmb_filter(self):
        """
        Test case for filtering variants for TMB calculation

        af_colname = 't_af'
        frequency_min = 0.05

        dp_colname = 't_depth'
        coverage_min = 500.0

        Need to report mutations that are NOT synonymous_variant EXCEPT for TERT promoter
        TERT promoter : gene == TERT, start_ge == 1295141, start_le == 1295340
        """
        self.maxDiff = None
        comments = [
        ['# comment 1'],
        ['# comment 2']
        ]
        row1 = {
        't_af': '0.50',
        't_depth': '550',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Consequence': 'synonymous_variant' # exclude due to synonymous_variant
        }
        row2 = {
        't_af': '0.50',
        't_depth': '550',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Consequence': 'splice_region_variant,synonymous_variant' # exclude due to synonymous_variant
        }
        row3 = { # this one should pass filter
        't_af': '0.50',
        't_depth': '550',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Consequence': 'missense_variant'
        }
        row4 = {
        't_af': '0.01', # exclude due to low AF
        't_depth': '550',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Consequence': 'missense_variant'
        }
        row5 = {
        't_af': '0.51',
        't_depth': '90', # exclude due to low coverage
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Consequence': 'missense_variant'
        }
        row6 = { # this one should pass filter
        't_af': '0.45',
        't_depth': '590',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Consequence': 'splice_region_variant'
        }
        row7 = { # this one should pass filter
        't_af': '0.45',
        't_depth': '590',
        'Hugo_Symbol': 'TERT',
        'Start_Position': '1295340', # good value; is_TERT_promoter = True
        'Consequence': 'splice_region_variant'
        }
        row8 = { # this should pass filter
        't_af': '0.45',
        't_depth': '590',
        'Hugo_Symbol': 'TERT',
        'Start_Position': '1295339', # good value; is_TERT_promoter = True
        'Consequence': 'splice_region_variant'
        }
        row9 = { # this should pass filter
        't_af': '0.45',
        't_depth': '590',
        'Hugo_Symbol': 'TERT',
        'Start_Position': '1295341', # bad value; is_TERT_promoter = False
        'Consequence': 'splice_region_variant' # include anyway because its not synonymous_variant
        }
        row10 ={ # this should pass filter
        't_af': '0.45',
        't_depth': '590',
        'Hugo_Symbol': 'TERT',
        'Start_Position': '1295339', # good value; is_TERT_promoter = True
        'Consequence': 'synonymous_variant' # include even though its synonymous_variant
        }

        maf_rows = [ row1, row2, row3, row4, row5, row6, row7, row8, row9, row10 ]
        maf_lines = dicts2lines(dict_list = maf_rows, comment_list = comments)
        input_file = write_table(self.tmpdir, filename = "input.maf", lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, input_file, output_file]
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)

        comments, mutations = load_mutations(output_file)

        expected_comments = ['# comment 1', '# comment 2']
        expected_mutations = [
        {'t_af': '0.50', 't_depth': '550', 'Consequence': 'missense_variant', 'Hugo_Symbol': 'EGFR', 'Start_Position': '1'},
        {'t_af': '0.45', 't_depth': '590', 'Consequence': 'splice_region_variant', 'Hugo_Symbol': 'EGFR', 'Start_Position': '1'},
        {'t_af': '0.45', 't_depth': '590', 'Consequence': 'splice_region_variant', 'Hugo_Symbol': 'TERT', 'Start_Position': '1295340'},
        {'t_af': '0.45', 't_depth': '590', 'Consequence': 'splice_region_variant', 'Hugo_Symbol': 'TERT', 'Start_Position': '1295339'},
        {'Consequence': 'splice_region_variant', 'Hugo_Symbol': 'TERT', 'Start_Position': '1295341', 't_af': '0.45', 't_depth': '590'},
        {'Consequence': 'synonymous_variant', 'Hugo_Symbol': 'TERT', 'Start_Position': '1295339', 't_af': '0.45', 't_depth': '590'}
        ]

        self.assertEqual(comments, expected_comments)
        self.assertEqual(mutations, expected_mutations)

    def test_tmb_filter2(self):
        """
        Test handling of messed up entries; t_af key missing
        """
        self.maxDiff = None
        # no t_af key, but has t_ref_count and t_alt_count
        row1 = { # this one should pass filter # 't_af': '0.50', # t_af not present
        't_ref_count': '275',
        't_alt_count': '275',
        't_depth': '550',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Consequence': 'missense_variant'
        }
        row2 = {
        't_ref_count': '275',
        't_alt_count': '275',
        't_depth': '550',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Consequence': 'missense_variant'
        }
        row3 = { # exclude due to low AF
        't_ref_count': '545',
        't_alt_count': '5',
        't_depth': '550',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Consequence': 'missense_variant'
        }
        maf_rows = [ row1, row2, row3 ]
        maf_lines = dicts2lines(dict_list = maf_rows, comment_list = [])
        input_file = write_table(self.tmpdir, filename = "input.maf", lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, input_file, output_file]
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)

        comments, mutations = load_mutations(output_file)

        expected_mutations = [
        {'t_depth': '550', 't_ref_count': '275', 't_alt_count': '275', 'Consequence': 'missense_variant', 'Hugo_Symbol': 'EGFR', 'Start_Position': '1'},
        {'t_depth': '550', 't_ref_count': '275', 't_alt_count': '275', 'Consequence': 'missense_variant', 'Hugo_Symbol': 'EGFR', 'Start_Position': '1'},
        ]

        self.assertEqual(mutations, expected_mutations)

    def test_tmb_filter3(self):
        """
        Test handling of messed up entries; t_af key missing and some t_depth are blank
        """
        self.maxDiff = None
        # no t_af key, but has t_ref_count and t_alt_count
        row1 = { # this one should pass filter # 't_af': '0.50', # t_af not present
        't_ref_count': '275',
        't_alt_count': '275',
        't_depth': '', # this one is blank
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Consequence': 'missense_variant'
        }
        row2 = {
        't_ref_count': '275',
        't_alt_count': '275',
        't_depth': '550',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '2',
        'Consequence': 'missense_variant'
        }
        row3 = { # exclude due to low AF
        't_ref_count': '545',
        't_alt_count': '5',
        't_depth': '550',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '3',
        'Consequence': 'missense_variant'
        }
        maf_rows = [ row1, row2, row3 ]
        maf_lines = dicts2lines(dict_list = maf_rows, comment_list = [])
        input_file = write_table(self.tmpdir, filename = "input.maf", lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, input_file, output_file]
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)

        comments, mutations = load_mutations(output_file)

        expected_mutations = [
        {'t_depth': '', 't_ref_count': '275', 't_alt_count': '275', 'Consequence': 'missense_variant', 'Hugo_Symbol': 'EGFR', 'Start_Position': '1'},
        {'t_depth': '550', 't_ref_count': '275', 't_alt_count': '275', 'Consequence': 'missense_variant', 'Hugo_Symbol': 'EGFR', 'Start_Position': '2'}
        ]

        self.assertEqual(mutations, expected_mutations)

    def test_tmb_filter4(self):
        """
        Test handling of mutation status in variants
        """
        self.maxDiff = None
        row1 = {
        't_ref_count': '275',
        't_alt_count': '275',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Mutation_Status': "GERMLINE",
        'Consequence': 'missense_variant'
        }
        row2 = { # this one should pass
        't_ref_count': '275',
        't_alt_count': '275',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '2',
        'Mutation_Status': "SOMATIC",
        'Consequence': 'missense_variant'
        }
        row3 = {
        't_ref_count': '275',
        't_alt_count': '275',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '3',
        'Mutation_Status': "UNKNOWN",
        'Consequence': 'missense_variant'
        }
        row4 = {
        't_ref_count': '275',
        't_alt_count': '275',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '4',
        'Mutation_Status': "",
        'Consequence': 'missense_variant'
        }
        maf_rows = [ row1, row2, row3, row4 ]
        maf_lines = dicts2lines(dict_list = maf_rows, comment_list = [])
        input_file = write_table(self.tmpdir, filename = "input.maf", lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, input_file, output_file]
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)

        comments, mutations = load_mutations(output_file)

        expected_mutations = [
        {'t_ref_count': '275', 't_alt_count': '275', 'Consequence': 'missense_variant', 'Hugo_Symbol': 'EGFR', 'Start_Position': '2', 'Mutation_Status': "SOMATIC"},
        {'t_ref_count': '275', 't_alt_count': '275', 'Consequence': 'missense_variant', 'Hugo_Symbol': 'EGFR', 'Start_Position': '4', 'Mutation_Status': ""},
        ]

        self.assertEqual(mutations, expected_mutations)

    def test_tmb_filter5(self):
        """
        Test handling of 0 depth for variant
        """
        self.maxDiff = None
        row1 = { # this one should fail
        't_ref_count': '0',
        't_alt_count': '0',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Mutation_Status': "SOMATIC",
        'Consequence': 'missense_variant'
        }
        row2 = { # this one should pass
        't_ref_count': '275',
        't_alt_count': '275',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '2',
        'Mutation_Status': "SOMATIC",
        'Consequence': 'missense_variant'
        }
        maf_rows = [ row1, row2 ]
        maf_lines = dicts2lines(dict_list = maf_rows, comment_list = [])
        input_file = write_table(self.tmpdir, filename = "input.maf", lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, input_file, output_file]
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)

        comments, mutations = load_mutations(output_file)

        expected_mutations = [
        {'t_ref_count': '275', 't_alt_count': '275', 'Consequence': 'missense_variant', 'Hugo_Symbol': 'EGFR', 'Start_Position': '2', 'Mutation_Status': "SOMATIC"}
        ]

        self.assertEqual(mutations, expected_mutations)

    def test_tmb_filter6(self):
        """
        Test handling of missing values for depths
        """
        self.maxDiff = None
        row1 = { # this one should fail
        't_ref_count': '0',
        't_alt_count': '0',
        't_af': '',
        't_depth': '',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '1',
        'Mutation_Status': "SOMATIC",
        'Consequence': 'missense_variant'
        }
        row2 = { # this one should pass
        't_ref_count': '275',
        't_alt_count': '275',
        't_af': '',
        't_depth': '',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '2',
        'Mutation_Status': "SOMATIC",
        'Consequence': 'missense_variant'
        }
        row3 = { # this one should fail
        't_ref_count': '275',
        't_alt_count': '',
        't_af': '',
        't_depth': '',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '3',
        'Mutation_Status': "SOMATIC",
        'Consequence': 'missense_variant'
        }
        row4 = { # this one should fail
        't_ref_count': '',
        't_alt_count': '275',
        't_af': '',
        't_depth': '',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '4',
        'Mutation_Status': "SOMATIC",
        'Consequence': 'missense_variant'
        }
        row5 = { # this one should pass
        't_ref_count': '225',
        't_alt_count': '275',
        't_af': '0.55',
        't_depth': '',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '5',
        'Mutation_Status': "SOMATIC",
        'Consequence': 'missense_variant'
        }
        row6 = { # this one should pass
        't_ref_count': '', # 225
        't_alt_count': '275',
        't_af': '', # '0.55',
        't_depth': '500',
        'Hugo_Symbol': 'EGFR',
        'Start_Position': '6',
        'Mutation_Status': "SOMATIC",
        'Consequence': 'missense_variant'
        }
        maf_rows = [ row1, row2, row3, row4, row5, row6 ]
        maf_lines = dicts2lines(dict_list = maf_rows, comment_list = [])
        input_file = write_table(self.tmpdir, filename = "input.maf", lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, input_file, output_file]
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)

        comments, mutations = load_mutations(output_file)

        expected_mutations = [
        {'t_ref_count': '275', 't_alt_count': '275', 't_af': '', 't_depth': '', 'Consequence': 'missense_variant', 'Hugo_Symbol': 'EGFR', 'Start_Position': '2', 'Mutation_Status': "SOMATIC"},
        {'t_ref_count': '225', 't_alt_count': '275', 't_af': '0.55', 't_depth': '', 'Hugo_Symbol': 'EGFR', 'Start_Position': '5', 'Mutation_Status': "SOMATIC", 'Consequence': 'missense_variant'},
        {'t_ref_count': '', 't_alt_count': '275', 't_af': '', 't_depth': '500', 'Hugo_Symbol': 'EGFR', 'Start_Position': '6', 'Mutation_Status': "SOMATIC", 'Consequence': 'missense_variant'}
        ]

        self.assertEqual(mutations, expected_mutations)

if __name__ == "__main__":
    unittest.main()
