#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for updating portal mutations
"""
import sys
import os
import unittest

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .settings import DATA_SETS

if __name__ == "__main__":
    from settings import DATA_SETS

# need to import the module from the other dir
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from bin.update_cBioPortal_data import update_mutation_data
sys.path.pop(0)

class TestGenerateCBioFiles(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
