#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for compiling a demo report
"""
import sys
import os
import unittest
import csv
import importlib
from pathlib import Path

# need to import the module from the other dir
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from pluto.tools import PlutoTestCase
from settings import REPORT_DIR
concat_tables = importlib.import_module("bin.concat-tables")
sys.path.pop(0)

compile_script = os.path.join(REPORT_DIR, 'compile.R')


class TestCompileReport(PlutoTestCase):
    def test_compile_demo_report(self):
        """
        Test case for making a demo of the HTML report
        """
        mut_lines = [
        ['Hugo_Symbol', 'Amino_Acid_Change', 'Tumor_Sample_Barcode'],
        ["TAP1", "A>T", "Sample1"],
        ]

        sample_lines = [
        ['#SAMPLE_ID', 'SPECIMEN_PRESERVATION_TYPE', 'ONCOTREE_CODE'],
        ['#SAMPLE_ID', 'SPECIMEN_PRESERVATION_TYPE', 'ONCOTREE_CODE'],
        ['#STRING', 'STRING', 'STRING'],
        ['#1', '1', '1'],
        ['SAMPLE_ID', 'SPECIMEN_PRESERVATION_TYPE', 'ONCOTREE_CODE'],
        ["Sample1", "FFPE", "MEL"],
        ]

        patient_lines = [
        ['#PATIENT_ID', 'SEX'],
        ['#PATIENT_ID', 'SEX'],
        ['#STRING', 'STRING'],
        ['#1', '1'],
        ['PATIENT_ID', 'SEX'],
        ['p_C_00001', 'F']
        ]

        mut_file = self.write_table(self.tmpdir, filename = "muts.txt", lines = mut_lines)
        sample_file = self.write_table(self.tmpdir, filename = "samples.txt", lines = sample_lines)
        patient_file = self.write_table(self.tmpdir, filename = "patients.txt", lines = patient_lines)
        output_file = os.path.join(self.tmpdir, "report.html")

        command = [
            compile_script,
            '--output_file', output_file,
            '--mutations', mut_file,
            '--samples', sample_file,
            '--patients', patient_file
        ]

        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)

        # print(proc_stdout)
        # print(proc_stderr)
        self.assertTrue(os.path.exists(output_file))


if __name__ == "__main__":
    unittest.main()
