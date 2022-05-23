#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cases for converting fusion files to sv format
"""
from settings import BIN_DIR
from pluto.tools import PlutoTestCase, TableReader
import os
import sys
import unittest

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
sys.path.pop(0)

script = os.path.join(BIN_DIR, 'fusion_to_sv_converter.py')


class TestConvertFusion(PlutoTestCase):
    def test_convert_fusion1(self):
        """
        Test case for converting a valid fusion file to sv format
        """
        lines1 = [
            ["Hugo_Symbol",	"Entrez_Gene_Id",	"Center	Tumor_Sample_Barcode",
                "Fusion",	"DNA_support	RNA_support	Method", "Frame"],
            ["IRF2BP2",	"359948",	"mskcc.org",	"sample1",
                "IRF2BP2-NTRK1 fusion", "yes",	"no",	"EMBL.DELLYv0.7.7",	"5to5"],
            ["NTRK1",	"4914",	"mskcc.org",	"sample1",	"IRF2BP2-NTRK1 fusion",
                "yes",	"no",	"EMBL.DELLYv0.7.7",	"5to5"],
            ["NTRK1",	"4914",	"mskcc.org",	"sample2",	"NTRK1-TPM3 fusion",
                "yes",	"no",	"EMBL.DELLYv0.7.7",	"5to5"],
            ["TPM3",	"7170",	"mskcc.org",	"sample2",	"NTRK1-TPM3 fusion",
                "yes",	"no",	"EMBL.DELLYv0.7.7",	"5to5"],
            ["IRF2BP2",	"359948",	"mskcc.org",	"sample3",
                "IRF2BP2-NTRK1 fusion", "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to3"],
            ["NTRK1",	"4914",	"mskcc.org",	"sample3",	"IRF2BP2-NTRK1 fusion",
                "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to3"],
            ["MTOR",	"2475",	"mskcc.org",	"sample4",	"MTOR-EXOSC10 fusion",
                "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to5"],
            ["EXOSC10",	"5394",	"mskcc.org",	"sample4",	"MTOR-EXOSC10 fusion",
                "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to5"],
            ["HIST1H1E",	"3008",	"mskcc.org",	"sample5",
                "HIST1H1E-HIST1H2BD fusion", "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to5"],
            ["HIST1H2BD",	"3017",	"mskcc.org",	"sample5",
                "HIST1H1E-HIST1H2BD fusion", "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to5"],
            ["CDKN2B",	"1030",	"mskcc.org",	"sample6",	"CDKN2B-CDKN2A fusion",
                "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to5"],
            ["CDKN2A",	"1029",	"mskcc.org",	"sample6",	"CDKN2B-CDKN2A fusion",
                "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to5"],
            ["ARHGAP9",	"64333",	"mskcc.org",	"sample7",
                "ARHGAP9-GLI1 fusion", "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to5"],
            ["GLI1",	"2735",	"mskcc.org",	"sample7",	"ARHGAP9-GLI1 fusion",
                "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to5"],
            ["HIST1H2BD",	"3017",	"mskcc.org",	"sample8",
                "HIST1H2BD-HIST1H1E fusion", "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to5"],
            ["HIST1H1E",	"3008",	"mskcc.org",	"sample8",
                "HIST1H2BD-HIST1H1E fusion", "yes",	"no",	"EMBL.DELLYv0.7.7",	"3to5"],
            ["KMT2C",	"58508",	"mskcc.org",	"sample9",	"KMT2C-HILPDA fusion",
                "yes",	"no",	"EMBL.DELLYv0.7.7",	"5to3"],
            ["HILPDA",	"29923",	"mskcc.org",	"sample9",	"KMT2C-HILPDA fusion",
                "yes",	"no",	"EMBL.DELLYv0.7.7",	"5to3"],

        ]

        table1 = self.write_table(
            self.tmpdir, filename="input_fusion.txt", lines=lines1)

        output_file = os.path.join(self.tmpdir, "output_sv.txt")
        command = [script, '--fusion_file', table1, '--sv_file', output_file]

        returncode, proc_stdout, proc_stderr = self.run_command(
            command, validate=True, testcase=self)

        # check the output file contents
        reader = TableReader(output_file)
        fieldnames = reader.get_fieldnames()
        records = [rec for rec in reader.read()]
        expected_records = [{'Sample_ID': 'sample1', 'Site1_Hugo_Symbol': 'IRF2BP2',
                             'Site1_Entrez_Gene_Id': '359948', 'Site2_Hugo_Symbol': 'NTRK1', 'Site2_Entrez_Gene_Id': '4914',
                             'SV_Status': 'SOMATIC', 'Center': 'mskcc.org', 'Event_Info': 'IRF2BP2-NTRK1 fusion', 'DNA_support': 'yes',
                             'RNA_support': 'no', 'Method': 'EMBL.DELLYv0.7.7', 'Site2_Effect_On_Frame': '5to5'},
                            {'Sample_ID': 'sample2', 'Site1_Hugo_Symbol': 'NTRK1', 'Site1_Entrez_Gene_Id': '4914', 'Site2_Hugo_Symbol': 'TPM3',
                             'Site2_Entrez_Gene_Id': '7170', 'SV_Status': 'SOMATIC', 'Center': 'mskcc.org', 'Event_Info': 'NTRK1-TPM3 fusion', 'DNA_support': 'yes',
                             'RNA_support': 'no', 'Method': 'EMBL.DELLYv0.7.7', 'Site2_Effect_On_Frame': '5to5'},
                            {'Sample_ID': 'sample3', 'Site1_Hugo_Symbol': 'IRF2BP2', 'Site1_Entrez_Gene_Id': '359948', 'Site2_Hugo_Symbol': 'NTRK1',
                             'Site2_Entrez_Gene_Id': '4914', 'SV_Status': 'SOMATIC', 'Center': 'mskcc.org', 'Event_Info': 'IRF2BP2-NTRK1 fusion', 'DNA_support': 'yes',
                             'RNA_support': 'no', 'Method': 'EMBL.DELLYv0.7.7', 'Site2_Effect_On_Frame': '3to3'},
                            {'Sample_ID': 'sample4', 'Site1_Hugo_Symbol': 'MTOR', 'Site1_Entrez_Gene_Id': '2475', 'Site2_Hugo_Symbol': 'EXOSC10',
                             'Site2_Entrez_Gene_Id': '5394', 'SV_Status': 'SOMATIC', 'Center': 'mskcc.org', 'Event_Info': 'MTOR-EXOSC10 fusion', 'DNA_support': 'yes',
                             'RNA_support': 'no', 'Method': 'EMBL.DELLYv0.7.7', 'Site2_Effect_On_Frame': '3to5'},
                            {'Sample_ID': 'sample5', 'Site1_Hugo_Symbol': 'HIST1H1E', 'Site1_Entrez_Gene_Id': '3008', 'Site2_Hugo_Symbol': 'HIST1H2BD',
                             'Site2_Entrez_Gene_Id': '3017', 'SV_Status': 'SOMATIC', 'Center': 'mskcc.org', 'Event_Info': 'HIST1H1E-HIST1H2BD fusion', 'DNA_support': 'yes',
                             'RNA_support': 'no', 'Method': 'EMBL.DELLYv0.7.7', 'Site2_Effect_On_Frame': '3to5'},
                            {'Sample_ID': 'sample6', 'Site1_Hugo_Symbol': 'CDKN2B', 'Site1_Entrez_Gene_Id': '1030', 'Site2_Hugo_Symbol': 'CDKN2A', 'Site2_Entrez_Gene_Id': '1029',
                             'SV_Status': 'SOMATIC', 'Center': 'mskcc.org', 'Event_Info': 'CDKN2B-CDKN2A fusion', 'DNA_support': 'yes',
                             'RNA_support': 'no', 'Method': 'EMBL.DELLYv0.7.7', 'Site2_Effect_On_Frame': '3to5'},
                            {'Sample_ID': 'sample7', 'Site1_Hugo_Symbol': 'ARHGAP9', 'Site1_Entrez_Gene_Id': '64333', 'Site2_Hugo_Symbol': 'GLI1', 'Site2_Entrez_Gene_Id': '2735',
                             'SV_Status': 'SOMATIC', 'Center': 'mskcc.org', 'Event_Info': 'ARHGAP9-GLI1 fusion', 'DNA_support': 'yes', 'RNA_support': 'no', 'Method': 'EMBL.DELLYv0.7.7',
                             'Site2_Effect_On_Frame': '3to5'},
                            {'Sample_ID': 'sample8', 'Site1_Hugo_Symbol': 'HIST1H2BD', 'Site1_Entrez_Gene_Id': '3017', 'Site2_Hugo_Symbol': 'HIST1H1E',
                             'Site2_Entrez_Gene_Id': '3008', 'SV_Status': 'SOMATIC', 'Center': 'mskcc.org', 'Event_Info': 'HIST1H2BD-HIST1H1E fusion', 'DNA_support': 'yes', 'RNA_support': 'no',
                             'Method': 'EMBL.DELLYv0.7.7', 'Site2_Effect_On_Frame': '3to5'},
                            {'Sample_ID': 'sample9', 'Site1_Hugo_Symbol': 'KMT2C', 'Site1_Entrez_Gene_Id': '58508', 'Site2_Hugo_Symbol': 'HILPDA', 'Site2_Entrez_Gene_Id': '29923', 'SV_Status': 'SOMATIC',
                             'Center': 'mskcc.org', 'Event_Info': 'KMT2C-HILPDA fusion', 'DNA_support': 'yes', 'RNA_support': 'no', 'Method': 'EMBL.DELLYv0.7.7', 'Site2_Effect_On_Frame': '5to3'}]

        self.assertEqual(records, expected_records)

    def test_convert_fusion_empty(self):
        """
        Test case for converting an empty fusion file to sv format
        """
        lines1 = [
            ["Hugo_Symbol",	"Entrez_Gene_Id",	"Center	Tumor_Sample_Barcode",
                "Fusion",	"DNA_support	RNA_support	Method", "Frame"]
        ]

        table1 = self.write_table(
            self.tmpdir, filename="input_fusion.txt", lines=lines1)

        output_file = os.path.join(self.tmpdir, "output_sv.txt")
        command = [script, '--fusion_file', table1, '--sv_file', output_file]

        returncode, proc_stdout, proc_stderr = self.run_command(
            command, validate=True, testcase=self)

        # check the output file contents
        reader = TableReader(output_file)
        fieldnames = reader.get_fieldnames()
        records = [rec for rec in reader.read()]
        expected_records = []

        self.assertEqual(records, expected_records)


if __name__ == "__main__":
    unittest.main()
