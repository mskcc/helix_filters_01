#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cases for updating samples fillout maf file script
"""
import sys
import os
import unittest

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from pluto.tools import PlutoTestCase
from settings import BIN_DIR
# from bin.update_cBioPortal_data import update_mutation_data
sys.path.pop(0)

script = os.path.join(BIN_DIR, 'update_fillout_maf.py')


class TestUpdateFilloutMaf(PlutoTestCase):
    def setUp(self):
        super().setUp()

        self.comments = [ # there must be 1 comment line for this input maf file
        ['# comment 1'],
        ]

        self.maf_row1 = {
        "Tumor_Sample_Barcode": "Sample1-T",
        "t_depth": "1", # has values; dont replace with fillout values
        "t_ref_count": "2",
        "t_alt_count": "3",
        "SRC": "Sample1-T,", # not a fillout; SRC contains Tumor_Sample_Barcode
        "t_FL_DP": "4",
        "t_FL_RD": "5",
        "t_FL_AD": "6"
        }
        self.maf_row2 = {
        "Tumor_Sample_Barcode": "Sample1-T",
        "t_depth": "", # doesnt have values; replace with fillout values
        "t_ref_count": "", # missing value should be empty string
        "t_alt_count": "",
        "SRC": "Sample1-T,", # not a fillout; SRC contains Tumor_Sample_Barcode
        "t_FL_DP": "4",
        "t_FL_RD": "5",
        "t_FL_AD": "6"
        }
        self.maf_row3 = {
        "Tumor_Sample_Barcode": "Sample1-T",
        "t_depth": "1", # has values; dont replace with fillout values
        "t_ref_count": "2",
        "t_alt_count": "3",
        "SRC": "Sample2-T,", # is a fillout; SRC doesnt contain Tumor_Sample_Barcode
        "t_FL_DP": "4",
        "t_FL_RD": "5",
        "t_FL_AD": "6"
        }

    def test_update_maf1(self):
        maf_rows = [ self.maf_row1, self.maf_row2, self.maf_row3 ]
        maf_lines = self.dicts2lines(dict_list = maf_rows, comment_list = self.comments)
        input_file = self.write_table(self.tmpdir, filename = "input.maf", lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, input_file, output_file]
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)

        comments, mutations = self.load_mutations(output_file)

        expected_comments = []
        expected_mutations = [
            {
            'Tumor_Sample_Barcode': 'Sample1-T',
            't_depth': '1',
            't_ref_count': '2',
            't_alt_count': '3',
            'SRC': 'Sample1-T,',
            't_FL_DP': '4',
            't_FL_RD': '5',
            't_FL_AD': '6',
            't_depth_sample': '1',
            't_ref_count_sample': '2',
            't_alt_count_sample': '3',
            'is_fillout': 'False'
            },
            {
            'Tumor_Sample_Barcode': 'Sample1-T',
            't_depth': '11',
            't_ref_count': '5',
            't_alt_count': '6',
            'SRC': 'Sample1-T,',
            't_FL_DP': '4',
            't_FL_RD': '5',
            't_FL_AD': '6',
            't_depth_sample': '',
            't_ref_count_sample': '',
            't_alt_count_sample': '',
            'is_fillout': 'False'
            },
            {
            'Tumor_Sample_Barcode': 'Sample1-T',
            't_depth': '1',
            't_ref_count': '2',
            't_alt_count': '3',
            'SRC': 'Sample2-T,',
            't_FL_DP': '4',
            't_FL_RD': '5',
            't_FL_AD': '6',
            't_depth_sample': '1',
            't_ref_count_sample': '2',
            't_alt_count_sample': '3',
            'is_fillout': 'True'
            }
        ]
        self.assertEqual(comments, expected_comments)
        self.assertEqual(mutations, expected_mutations)


if __name__ == "__main__":
    unittest.main()
