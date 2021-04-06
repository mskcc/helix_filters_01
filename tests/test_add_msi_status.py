#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cases for adding msi status to msi tables
"""
import os
import sys
import unittest

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from pluto.tools import PlutoTestCase, TableReader
from settings import BIN_DIR
sys.path.pop(0)

script = os.path.join(BIN_DIR, 'add_msi_status.py')

class TestAddMSIStatus(PlutoTestCase):
    def test_add_status1(self):
        """
        Test case for example of add msi status
        """
        lines1 = [
            ['Total_Number_of_Sites', 'Number_of_Somatic_Sites', 'MSI_SCORE', 'SAMPLE_ID'],
            ['123',                   '987',                     '11',     'Sample1-T'],
            ['456',                   '654',                     '2',      'Sample2-T'],
            ['789',                   '321',                     '5',      'Sample3-T']
        ]

        table1 = self.write_table(self.tmpdir, filename = "input_msi_table.tsv", lines = lines1)

        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, '-i', table1, '-o', output_file, '--header', 'MSI_STATUS']

        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)

        # check the output file contents
        reader = TableReader(output_file)
        fieldnames = reader.get_fieldnames()
        records = [ rec for rec in reader.read() ]
        expected_records = [
            {'Total_Number_of_Sites': '123', 'Number_of_Somatic_Sites': '987', 'MSI_SCORE': '11', 'SAMPLE_ID': 'Sample1-T', 'MSI_STATUS': 'Instable'},
            {'Total_Number_of_Sites': '456', 'Number_of_Somatic_Sites': '654', 'MSI_SCORE': '2',  'SAMPLE_ID': 'Sample2-T', 'MSI_STATUS': 'Stable'},
            {'Total_Number_of_Sites': '789', 'Number_of_Somatic_Sites': '321', 'MSI_SCORE': '5',  'SAMPLE_ID': 'Sample3-T', 'MSI_STATUS': 'Indeterminate'}
        ]
        self.assertEqual(records, expected_records)


    def test_add_empty_status1(self):
        """
        Add MSI status when the results values are 0
        """
        lines = [
        ['Total_Number_of_Sites', 'Number_of_Somatic_Sites', 'MSI_SCORE', 'SAMPLE_ID'],
        ['0', "0", '-nan', 'Sample1'],
        ['0', '0', '-nan', 'Sample2'],
        ['0', '0', '-nan', 'Sample3']
        ]
        table = self.write_table(self.tmpdir, filename = "input.tsv", lines = lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, '-i', table, '-o', output_file, '--header', 'MSI_STATUS']

        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)

        reader = TableReader(output_file)
        fieldnames = reader.get_fieldnames()
        records = [ rec for rec in reader.read() ]
        expected_records = [
            {'Total_Number_of_Sites': '0', 'Number_of_Somatic_Sites': '0', 'MSI_SCORE': '-nan', 'SAMPLE_ID': 'Sample1', 'MSI_STATUS': 'NA'},
            {'Total_Number_of_Sites': '0', 'Number_of_Somatic_Sites': '0', 'MSI_SCORE': '-nan',  'SAMPLE_ID': 'Sample2', 'MSI_STATUS': 'NA'},
            {'Total_Number_of_Sites': '0', 'Number_of_Somatic_Sites': '0', 'MSI_SCORE': '-nan',  'SAMPLE_ID': 'Sample3', 'MSI_STATUS': 'NA'}
        ]
        self.assertEqual(records, expected_records)






if __name__ == "__main__":
    unittest.main()
