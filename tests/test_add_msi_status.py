#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cases for merging tables
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

script = os.path.join(BIN_DIR, 'merge-tables.py')

class TestTMBVariantFilter(PlutoTestCase):
    def test_merge_tables1(self):
        """
        Test case for example of simple table merge
        """
        lines1 = [
            ['# comment 1'],
            ['# comment 2'],
            ['Sample', 'Frequency'],
            ['Sample1', '0.1'],
            ['Sample2', '0.2'],
            ['Sample3', '0.3']
        ]
        lines2 = [
            ['# comment 3'],
            ['# comment 4'],
            ['Sample', 'Depth'],
            ['Sample1', '100'],
            ['Sample2', '200'],
            ['Sample3', '300']
        ]
        table1 = self.write_table(self.tmpdir, filename = "table1.tsv", lines = lines1)
        table2 = self.write_table(self.tmpdir, filename = "table2.tsv", lines = lines2)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, table1, table2, '--key1', 'Sample', '--key2', 'Sample', '--output', output_file]
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)

        # check the output file contents
        reader = TableReader(output_file)
        comments = reader.comment_lines
        fieldnames = reader.get_fieldnames()
        records = [ rec for rec in reader.read() ]
        expected_comments = ['# comment 1\n', '# comment 2\n', '# comment 3\n', '# comment 4\n']
        expected_records = [
            {'Sample': 'Sample1', 'Frequency': '0.1', 'Depth': '100'},
            {'Sample': 'Sample2', 'Frequency': '0.2', 'Depth': '200'},
            {'Sample': 'Sample3', 'Frequency': '0.3', 'Depth': '300'}
        ]
        self.assertEqual(comments, expected_comments)
        self.assertEqual(records, expected_records)

    def test_merge_tables_tmb_data_clinical1(self):
        """
        Test case for merging example cBioPortal data clinical file with TMB data file

        NOTE: need to use header key 'CMO_TMB_SCORE' in table2 for cBioPortal mode to work !!
        """
        lines1 = [
        ['#SAMPLE_ID', 'PATIENT_ID', 'SAMPLE_COVERAGE'],
        ['#SAMPLE_ID', 'PATIENT_ID', 'SAMPLE_COVERAGE'],
        ['#STRING', 'STRING', 'NUMBER',],
        ['#1', '1', '1'],
        ['SAMPLE_ID', 'PATIENT_ID', 'SAMPLE_COVERAGE'],
        ['Sample1', 'Patient1', '108'],
        ['Sample2', 'Patient2', '502'],
        ['Sample3', 'Patient3', '256'],
        ]

        lines2 = [
        ['SampleID', 'CMO_TMB_SCORE'],
        ['Sample1', '100'],
        ['Sample2', '200'],
        ['Sample3', '300'],
        ]

        data_clinical_file = self.write_table(self.tmpdir, filename = "data_clinical_sample.txt", lines = lines1)
        tmb_file = self.write_table(self.tmpdir, filename = "tmb.tsv", lines = lines2)
        output_file = os.path.join(self.tmpdir, "data_clinical_sample.merged.txt")
        command = [script, data_clinical_file, tmb_file, '--key1', 'SAMPLE_ID', '--key2', 'SampleID', '--output', output_file, '--cBioPortal']
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)

        reader = TableReader(output_file)
        comments = reader.comment_lines
        fieldnames = reader.get_fieldnames()
        records = [ rec for rec in reader.read() ]
        expected_comments = [
            '#SAMPLE_ID\tPATIENT_ID\tSAMPLE_COVERAGE\tCMO_TMB_SCORE\n',
            '#SAMPLE_ID\tPATIENT_ID\tSAMPLE_COVERAGE\tCMO_TMB_SCORE\n',
            '#STRING\tSTRING\tNUMBER\tNUMBER\n',
            '#1\t1\t1\t1\n'
        ]
        expected_records = [
            {'SAMPLE_ID': 'Sample1', 'PATIENT_ID': 'Patient1', 'SAMPLE_COVERAGE': '108', 'CMO_TMB_SCORE': '100'},
            {'SAMPLE_ID': 'Sample2', 'PATIENT_ID': 'Patient2', 'SAMPLE_COVERAGE': '502', 'CMO_TMB_SCORE': '200'},
            {'SAMPLE_ID': 'Sample3', 'PATIENT_ID': 'Patient3', 'SAMPLE_COVERAGE': '256', 'CMO_TMB_SCORE': '300'}
        ]
        self.assertEqual(comments, expected_comments)
        self.assertEqual(records, expected_records)

    def test_merge_tables_tmb_data_clinical2(self):
        """
        Test case for merging a TMB table into a cBioPortal data clincial file when the former lacks some rows in the latter,
        and the first row of data clinical file contains a sample not in the TMB table
        """
        lines1 = [
        ['#SAMPLE_ID', 'PATIENT_ID', 'SAMPLE_COVERAGE'],
        ['#SAMPLE_ID', 'PATIENT_ID', 'SAMPLE_COVERAGE'],
        ['#STRING', 'STRING', 'NUMBER',],
        ['#1', '1', '1'],
        ['SAMPLE_ID', 'PATIENT_ID', 'SAMPLE_COVERAGE'],
        ['Sample1', 'Patient1', '108'],
        ['Sample2', 'Patient2', '502'],
        ['Sample3', 'Patient3', '256'],
        ]

        lines2 = [
        ['SampleID', 'CMO_TMB_SCORE'],
        ['Sample2', '200'],
        ['Sample3', '300'],
        ]

        data_clinical_file = self.write_table(self.tmpdir, filename = "data_clinical_sample.txt", lines = lines1)
        tmb_file = self.write_table(self.tmpdir, filename = "tmb.tsv", lines = lines2)
        output_file = os.path.join(self.tmpdir, "data_clinical_sample.merged.txt")
        command = [script, data_clinical_file, tmb_file, '--key1', 'SAMPLE_ID', '--key2', 'SampleID', '--output', output_file, '--cBioPortal']
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)

        reader = TableReader(output_file)
        comments = reader.comment_lines
        fieldnames = reader.get_fieldnames()
        records = [ rec for rec in reader.read() ]
        expected_comments = [
            '#SAMPLE_ID\tPATIENT_ID\tSAMPLE_COVERAGE\tCMO_TMB_SCORE\n',
            '#SAMPLE_ID\tPATIENT_ID\tSAMPLE_COVERAGE\tCMO_TMB_SCORE\n',
            '#STRING\tSTRING\tNUMBER\tNUMBER\n',
            '#1\t1\t1\t1\n'
        ]
        expected_records = [
            {'SAMPLE_ID': 'Sample1', 'PATIENT_ID': 'Patient1', 'SAMPLE_COVERAGE': '108', 'CMO_TMB_SCORE': 'NA'},
            {'SAMPLE_ID': 'Sample2', 'PATIENT_ID': 'Patient2', 'SAMPLE_COVERAGE': '502', 'CMO_TMB_SCORE': '200'},
            {'SAMPLE_ID': 'Sample3', 'PATIENT_ID': 'Patient3', 'SAMPLE_COVERAGE': '256', 'CMO_TMB_SCORE': '300'}
        ]
        self.assertEqual(comments, expected_comments)
        self.assertEqual(records, expected_records)

    def test_merge_tables_tmb_data_clinical_with_normals(self):
        """
        Test case for merging a TMB file with only tumors against a data clinical file that containes tumors and normals
        The output files leaves a blank for the missing values in table1
        """
        lines1 = [
        ['SAMPLE_ID', 'PATIENT_ID', 'SAMPLE_COVERAGE'],
        ['Sample1-T', 'Patient1', '108'],
        ['Sample1-N', 'Patient2', '58'],
        ['Sample2-T', 'Patient3', '502'],
        ['Sample2-N', 'Patient4', '56'],
        ]

        lines2 = [
        ['SampleID', 'TMB'],
        ['Sample1-T', '100'],
        ['Sample2-T', '200'],
        ]

        data_clinical_file = self.write_table(self.tmpdir, filename = "data_clinical_sample.txt", lines = lines1)
        tmb_file = self.write_table(self.tmpdir, filename = "tmb.tsv", lines = lines2)
        output_file = os.path.join(self.tmpdir, "data_clinical_sample.merged.txt")
        command = [script, data_clinical_file, tmb_file, '--key1', 'SAMPLE_ID', '--key2', 'SampleID', '--output', output_file]
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)

        reader = TableReader(output_file)
        comments = reader.comment_lines
        fieldnames = reader.get_fieldnames()
        records = [ rec for rec in reader.read() ]
        expected_comments = []
        expected_records = [
            {'SAMPLE_ID': 'Sample1-T', 'PATIENT_ID': 'Patient1', 'SAMPLE_COVERAGE': '108', 'TMB': '100'},
            {'SAMPLE_ID': 'Sample1-N', 'PATIENT_ID': 'Patient2', 'SAMPLE_COVERAGE': '58', 'TMB': 'NA'},
            {'SAMPLE_ID': 'Sample2-T', 'PATIENT_ID': 'Patient3', 'SAMPLE_COVERAGE': '502', 'TMB': '200'},
            {'SAMPLE_ID': 'Sample2-N', 'PATIENT_ID': 'Patient4', 'SAMPLE_COVERAGE': '56', 'TMB': 'NA'}
        ]
        self.assertEqual(comments, expected_comments)
        self.assertEqual(records, expected_records)

if __name__ == "__main__":
    unittest.main()
