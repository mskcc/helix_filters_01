#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cases for updating portal mutations
"""
import sys
import os
import unittest
from tempfile import TemporaryDirectory

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command, load_mutations, write_table, dicts2lines
    from .settings import BIN_DIR

if __name__ == "__main__":
    from tools import run_command, load_mutations, write_table, dicts2lines
    from settings import BIN_DIR

# need to import the module from the other dir
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from bin.update_cBioPortal_data import update_mutation_data
sys.path.pop(0)

portal_script = os.path.join(BIN_DIR, 'update_cBioPortal_data.py')

class TestUpdateCBioFiles(unittest.TestCase):
    def test_update_mutation_data(self):
        """
        Test that new rows are added correctly to the mutation data file
        """
        mut_data = {
        'tcn': "2",
        "lcn": "1",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375"
        }
        new_data = update_mutation_data(mut_data)
        expected_data = {
        'tcn': "2",
        "lcn": "1",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375",
        'ASCN.TOTAL_COPY_NUMBER': "2",
        'ASCN.MINOR_COPY_NUMBER': "1",
        'ASCN.EXPECTED_ALT_COPIES': "4",
        "ASCN.CCF_EXPECTED_COPIES": "0.127",
        "ASCN.CCF_EXPECTED_COPIES_LOWER": "0.615",
        "ASCN.CCF_EXPECTED_COPIES_UPPER": "0.375",
        "ASCN.ASCN_METHOD": "FACETS",
        "ASCN.ASCN_INTEGER_COPY_NUMBER": 'NA'
        }
        self.maxDiff = None
        self.assertDictEqual(new_data, expected_data)

        # add tumor ID to the mut data and include facets data
        mut_data = {
        'tumor': "Tumor1",
        'tcn': "2",
        "lcn": "1",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375"
        }
        facets_data = {
        'Tumor1': {
            "genome_doubled": 'TRUE'
            },
        'Tumor2': {
            "genome_doubled": 'FALSE'
            }
        }
        new_data = update_mutation_data(mut_data, facets_data)
        expected_data = {
        'tumor': "Tumor1",
        'tcn': "2",
        "lcn": "1",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375",
        'ASCN.TOTAL_COPY_NUMBER': "2",
        'ASCN.MINOR_COPY_NUMBER': "1",
        'ASCN.EXPECTED_ALT_COPIES': "4",
        "ASCN.CCF_EXPECTED_COPIES": "0.127",
        "ASCN.CCF_EXPECTED_COPIES_LOWER": "0.615",
        "ASCN.CCF_EXPECTED_COPIES_UPPER": "0.375",
        "ASCN.ASCN_METHOD": "FACETS",
        "ASCN.ASCN_INTEGER_COPY_NUMBER": '-1',
        }
        self.assertDictEqual(new_data, expected_data)

        # add sample ID and facets data
        mut_data = {
        'sample': "Tumor2",
        'tcn': "2",
        "lcn": "1",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375"
        }
        facets_data = {
        'Tumor1': {
            "genome_doubled": 'TRUE',
            },
        'Tumor2': {
            "genome_doubled": 'FALSE',
            }
        }
        new_data = update_mutation_data(mut_data, facets_data)
        expected_data = {
        'sample': "Tumor2",
        'tcn': "2",
        "lcn": "1",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375",
        'ASCN.TOTAL_COPY_NUMBER': "2",
        'ASCN.MINOR_COPY_NUMBER': "1",
        'ASCN.EXPECTED_ALT_COPIES': "4",
        "ASCN.CCF_EXPECTED_COPIES": "0.127",
        "ASCN.CCF_EXPECTED_COPIES_LOWER": "0.615",
        "ASCN.CCF_EXPECTED_COPIES_UPPER": "0.375",
        "ASCN.ASCN_METHOD": "FACETS",
        "ASCN.ASCN_INTEGER_COPY_NUMBER": '0',
        }
        self.assertDictEqual(new_data, expected_data)

        # no tumor or sample ID present in mutation data, but pass as arg instead
        # add sample ID and facets data
        mut_data = {
        'tcn': "2",
        "lcn": "0",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375"
        }
        facets_data = {
        'Tumor1': {
            "genome_doubled": 'TRUE',
            },
        'Tumor2': {
            "genome_doubled": 'FALSE',
            }
        }
        new_data = update_mutation_data(mut_data, facets_data, sample_id = "Tumor2")
        expected_data = {
        'tcn': "2",
        "lcn": "0",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375",
        'ASCN.TOTAL_COPY_NUMBER': "2",
        'ASCN.MINOR_COPY_NUMBER': "0",
        'ASCN.EXPECTED_ALT_COPIES': "4",
        "ASCN.CCF_EXPECTED_COPIES": "0.127",
        "ASCN.CCF_EXPECTED_COPIES_LOWER": "0.615",
        "ASCN.CCF_EXPECTED_COPIES_UPPER": "0.375",
        "ASCN.ASCN_METHOD": "FACETS",
        "ASCN.ASCN_INTEGER_COPY_NUMBER": '-1',
        }
        self.assertDictEqual(new_data, expected_data)

        # test that if one of the needed values is not a valid number, return None or NA strings
        mut_data = {
        'tcn': "NA",
        "lcn": "0",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375"
        }
        facets_data = {
        'Tumor1': {
            "genome_doubled": 'TRUE',
            },
        'Tumor2': {
            "genome_doubled": 'FALSE',
            }
        }
        new_data = update_mutation_data(mut_data, facets_data, sample_id = "Tumor2")
        expected_data = {
        'tcn': "NA", # <- this is now NA
        "lcn": "0",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375",
        'ASCN.TOTAL_COPY_NUMBER': "NA", # <- this is now NA
        'ASCN.MINOR_COPY_NUMBER': "0",
        'ASCN.EXPECTED_ALT_COPIES': "4",
        "ASCN.CCF_EXPECTED_COPIES": "0.127",
        "ASCN.CCF_EXPECTED_COPIES_LOWER": "0.615",
        "ASCN.CCF_EXPECTED_COPIES_UPPER": "0.375",
        "ASCN.ASCN_METHOD": "FACETS",
        "ASCN.ASCN_INTEGER_COPY_NUMBER": 'NA',
        }
        self.assertDictEqual(new_data, expected_data)


        # test handling for sets of values that are not in the key
        # mcn = tcn - lcn
        # numeric_call = str(facets_call_states[(wgd, mcn, lcn)])
        # KeyError: ('TRUE', 2, 3)
        mut_data = {
        'tcn': "1",
        "lcn": "3",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375"
        }
        facets_data = {
        'Tumor1': {
            "genome_doubled": 'TRUE',
            },
        'Tumor2': {
            "genome_doubled": 'FALSE',
            }
        }
        new_data = update_mutation_data(mut_data, facets_data, sample_id = "Tumor1")
        expected_data = {
        'tcn': "1",
        "lcn": "3",
        "expected_alt_copies": "4",
        "ccf_expected_copies": "0.127",
        "ccf_expected_copies_lower": "0.615",
        "ccf_expected_copies_upper": "0.375",
        'ASCN.TOTAL_COPY_NUMBER': "1",
        'ASCN.MINOR_COPY_NUMBER': "3",
        'ASCN.EXPECTED_ALT_COPIES': "4",
        "ASCN.CCF_EXPECTED_COPIES": "0.127",
        "ASCN.CCF_EXPECTED_COPIES_LOWER": "0.615",
        "ASCN.CCF_EXPECTED_COPIES_UPPER": "0.375",
        "ASCN.ASCN_METHOD": "FACETS",
        "ASCN.ASCN_INTEGER_COPY_NUMBER": 'NA',
        }
        self.assertDictEqual(new_data, expected_data)

class TestUpdateCBioMaf(unittest.TestCase):
    """
    Test case for updating the data_mutations_extended.txt maf file with columns from the Facets maf file
    """
    def setUp(self):
        self.maf_row1 = {
        "Hugo_Symbol" : "FGF3",
        "Entrez_Gene_Id" : "2248",
        "Chromosome" : "11",
        "Start_Position" : "69625447",
        "End_Position": "69625448",
        "Tumor_Sample_Barcode": "Sample1-T",
        "Matched_Norm_Sample_Barcode": "Sample1-N",
        "portal_val": "foo" # dummy value that would only be in portal data_mutations_extended.txt output maf file
        }
        self.maf_row2 = {
        "Hugo_Symbol" : "PNISR",
        "Entrez_Gene_Id" : "25957",
        "Chromosome" : "6",
        "Start_Position" : "99865784",
        "End_Position": "99865785",
        "Tumor_Sample_Barcode": "Sample1-T",
        "Matched_Norm_Sample_Barcode": "Sample1-N",
        "portal_val": "foo" # dummy value that would only be in portal data_mutations_extended.txt output maf file
        }
        self.maf_row3 = { # extra row with no match in facets
        "Hugo_Symbol" : "PNISR",
        "Entrez_Gene_Id" : "25957",
        "Chromosome" : "6",
        "Start_Position" : "99865788",
        "End_Position": "99865789",
        "Tumor_Sample_Barcode": "Sample1-T",
        "Matched_Norm_Sample_Barcode": "Sample1-N",
        "portal_val": "foo" # dummy value that would only be in portal data_mutations_extended.txt output maf file
        }
        self.facets_row1 = {
        "Hugo_Symbol" : "FGF3",
        "Entrez_Gene_Id" : "2248",
        "Chromosome" : "11",
        "Start_Position" : "69625447",
        "End_Position": "69625448",
        "Tumor_Sample_Barcode": "Sample1-T",
        "Matched_Norm_Sample_Barcode": "Sample1-N",
        "ASCN.TOTAL_COPY_NUMBER": "1" # dummy value that would only be in facets Tumor1.Normal1_hisens.ccf.maf output maf file
        }
        self.facets_row2 = {
        "Hugo_Symbol" : "PNISR",
        "Entrez_Gene_Id" : "25957",
        "Chromosome" : "6",
        "Start_Position" : "99865784",
        "End_Position": "99865785",
        "Tumor_Sample_Barcode": "Sample1-T",
        "Matched_Norm_Sample_Barcode": "Sample1-N",
        "ASCN.TOTAL_COPY_NUMBER": "2" # dummy value that would only be in facets Tumor1.Normal1_hisens.ccf.maf output maf file
        }
        self.facets_row3 = { # extra row with no match in maf
        "Hugo_Symbol" : "PNISR2",
        "Entrez_Gene_Id" : "25957",
        "Chromosome" : "6",
        "Start_Position" : "99865784",
        "End_Position": "99865785",
        "Tumor_Sample_Barcode": "Sample1-T",
        "Matched_Norm_Sample_Barcode": "Sample1-N",
        "ASCN.TOTAL_COPY_NUMBER": "2" # dummy value that would only be in facets Tumor1.Normal1_hisens.ccf.maf output maf file
        }

        self.demo_comments = [
        ['# comment 1'],
        ['# comment 2']
        ]

    def test_merge_facets_portal_maf(self):
        """
        Integration test for merging a cBioPortal data_mutations_extended.txt maf with the Facets maf
        """
        self.maxDiff = None
        # make sets of lines to write to tables
        maf_rows = [ self.maf_row1, self.maf_row2, self.maf_row3 ]
        maf_lines = dicts2lines(dict_list = maf_rows, comment_list = self.demo_comments)

        facets_rows = [ self.facets_row1, self.facets_row2, self.facets_row3 ]
        facets_lines = dicts2lines(dict_list = facets_rows, comment_list = self.demo_comments)

        with TemporaryDirectory() as tmpdir:
            input_maf_file = write_table(tmpdir, filename = "input.maf", lines = maf_lines)
            input_facets_file = write_table(tmpdir, filename = "facets.maf", lines = facets_lines)
            output_file = os.path.join(tmpdir, "output.txt")
            command = [ portal_script, 'merge_mafs', '--input', input_maf_file, '--facets-maf', input_facets_file, '--output', output_file ]

            # run the script in a subprocess
            returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)

            comments, mutations = load_mutations(output_file)
            expected_comments = [ '# comment 1', '# comment 2' ]
            self.assertEqual(comments, expected_comments)
            expected_mutations = [
                {
                "Hugo_Symbol" : "FGF3",
                "Entrez_Gene_Id" : "2248",
                "Chromosome" : "11",
                "Start_Position" : "69625447",
                "End_Position": "69625448",
                "Tumor_Sample_Barcode": "Sample1-T",
                "Matched_Norm_Sample_Barcode": "Sample1-N",
                "portal_val": "foo",
                "ASCN.CLONAL": "1"
                },
                {
                "Hugo_Symbol" : "PNISR",
                "Entrez_Gene_Id" : "25957",
                "Chromosome" : "6",
                "Start_Position" : "99865784",
                "End_Position": "99865785",
                "Tumor_Sample_Barcode": "Sample1-T",
                "Matched_Norm_Sample_Barcode": "Sample1-N",
                "portal_val": "foo",
                "ASCN.CLONAL": "2"
                },
                {
                "Hugo_Symbol" : "PNISR",
                "Entrez_Gene_Id" : "25957",
                "Chromosome" : "6",
                "Start_Position" : "99865788",
                "End_Position": "99865789",
                "Tumor_Sample_Barcode": "Sample1-T",
                "Matched_Norm_Sample_Barcode": "Sample1-N",
                "portal_val": "foo",
                "ASCN.CLONAL": "."
                }
            ]
            self.assertEqual(mutations, expected_mutations)

if __name__ == "__main__":
    unittest.main()
