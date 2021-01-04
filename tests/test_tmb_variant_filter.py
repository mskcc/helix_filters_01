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
        comments = [
        ['# comment 1'],
        ['# comment 2']
        ]
        row1 = {
        't_af': '0.50',
        't_depth': '550',
        'Consequence': 'synonymous_variant' # exclude due to synonymous_variant
        }
        row2 = {
        't_af': '0.50',
        't_depth': '550',
        'Consequence': 'splice_region_variant,synonymous_variant' # exclude due to synonymous_variant
        }
        row3 = { # this one should pass filter
        't_af': '0.50',
        't_depth': '550',
        'Consequence': 'missense_variant'
        }
        row4 = {
        't_af': '0.01', # exclude due to low AF
        't_depth': '550',
        'Consequence': 'missense_variant'
        }
        row5 = {
        't_af': '0.51',
        't_depth': '90', # exclude due to low coverage
        'Consequence': 'missense_variant'
        }
        row6 = { # this one should pass filter
        't_af': '0.45',
        't_depth': '590',
        'Consequence': 'splice_region_variant'
        }
        maf_rows = [ row1, row2, row3, row4, row5, row6 ]
        maf_lines = dicts2lines(dict_list = maf_rows, comment_list = comments)
        input_file = write_table(self.tmpdir, filename = "input.maf", lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, input_file, output_file]
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)

        comments, mutations = load_mutations(output_file)

        expected_comments = ['# comment 1', '# comment 2']
        expected_mutations = [
        {'t_af': '0.50', 't_depth': '550', 'Consequence': 'missense_variant'},
        {'t_af': '0.45', 't_depth': '590', 'Consequence': 'splice_region_variant'}
        ]

        self.assertEqual(comments, expected_comments)
        self.assertEqual(mutations, expected_mutations)

if __name__ == "__main__":
    unittest.main()
