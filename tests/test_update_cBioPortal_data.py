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
from bin.update_cBioPortal_data import parse_facets_data
from bin.update_cBioPortal_data import update_sample_data
from bin.update_cBioPortal_data import update_mutation_data
sys.path.pop(0)

class TestGenerateCBioFiles(unittest.TestCase):
    def test_parse_facets_data1(self):
        """
        test that a list of dicts output from Facets Suite can be loaded correctly
        should return a dict with only "hisens" data
        This simulates how data should be loaded from the Facets Suite .txt output files
        """
        facets_data = [
            {
                'hypoploid': 'FALSE',
                'run_type': 'purity',
                'fraction_loh': '0.21',
                'facets_version': '0.5.14',
                'hrd_loh': '1',
                'snp_nbhd': '250',
                'genome_doubled': 'TRUE',
                'ndepth': '35',
                'dipLogR': '-1.1',
                'sample': 'Tumor1.Normal1',
                'lst': '1',
                'seed': '1000',
                'flags': 'mafR not sufficiently small',
                'purity': '0.35',
                'input_file': 'Tumor1.Normal1.snp_pileup.gz',
                'ntai': '2',
                'fraction_cna': '1',
                'min_nhet': '25',
                'ploidy': '8.1',
                'cval': '100',
                'genome': 'hg19'
            },
            {
                'hypoploid': 'FALSE',
                'run_type': 'hisens',
                'fraction_loh': '0.22',
                'facets_version': '0.5.14',
                'hrd_loh': '3',
                'snp_nbhd': '250',
                'genome_doubled': 'TRUE',
                'ndepth': '35',
                'dipLogR': '-1.1',
                'sample': 'Tumor1.Normal1',
                'lst': '5',
                'seed': '1000',
                'flags': '',
                'purity': '0.36',
                'input_file': 'Tumor1.Normal1.snp_pileup.gz',
                'ntai': '6',
                'fraction_cna': '0.92',
                'min_nhet': '25',
                'ploidy': '7.9',
                'cval': '50',
                'genome': 'hg19'
            },
            {
                'hypoploid': 'FALSE',
                'run_type': 'purity',
                'fraction_loh': '0.21',
                'facets_version': '0.5.14',
                'hrd_loh': '1',
                'snp_nbhd': '250',
                'genome_doubled': 'FALSE',
                'ndepth': '35',
                'dipLogR': '-1.1',
                'sample': 'Tumor2.Normal2',
                'lst': '1',
                'seed': '1000',
                'flags': 'mafR not sufficiently small',
                'purity': '0.35',
                'input_file': 'Tumor2.Normal2.snp_pileup.gz',
                'ntai': '2',
                'fraction_cna': '1',
                'min_nhet': '25',
                'ploidy': '8.1',
                'cval': '100',
                'genome': 'hg19'
            },
            {
                'hypoploid': 'FALSE',
                'run_type': 'hisens',
                'fraction_loh': '0.22',
                'facets_version': '0.5.14',
                'hrd_loh': '3',
                'snp_nbhd': '250',
                'genome_doubled': 'FALSE',
                'ndepth': '35',
                'dipLogR': '-1.1',
                'sample': 'Tumor2.Normal2',
                'lst': '5',
                'seed': '1000',
                'flags': '',
                'purity': '0.36',
                'input_file': 'Tumor2.Normal2.snp_pileup.gz',
                'ntai': '6',
                'fraction_cna': '0.92',
                'min_nhet': '25',
                'ploidy': '7.9',
                'cval': '50',
                'genome': 'hg19'
            }
            ]
        parsed_data = parse_facets_data(facets_data)
        expected_data = {
        'Tumor1': {
            "purity": "0.36",
            "ploidy" : '7.9',
            "facets_version": '0.5.14',
            "genome_doubled": 'TRUE',
            "ASCN_PURITY": "0.36",
            "ASCN_PLOIDY": '7.9',
            "ASCN_VERSION": '0.5.14',
            "ASCN_WGD": "WGD"
            },
        'Tumor2': {
            "purity": "0.36",
            "ploidy" : '7.9',
            "facets_version": '0.5.14',
            "genome_doubled": 'FALSE',
            "ASCN_PURITY": "0.36",
            "ASCN_PLOIDY": '7.9',
            "ASCN_VERSION": '0.5.14',
            "ASCN_WGD": "no WGD"
            }
        }
        self.maxDiff = None
        self.assertDictEqual(parsed_data, expected_data)


    def test_update_sample_data(self):
        """
        Tests for updating the data from data_clinical_sample.txt file with corresponding data loaded from the Facets Suite output .txt file
        """
        facets_data = {
        'Tumor1': {
            "purity": "0.36",
            "ploidy" : '7.9',
            "facets_version": '0.5.14',
            "genome_doubled": 'TRUE',
            "ASCN_PURITY": "0.36",
            "ASCN_PLOIDY": '7.9',
            "ASCN_VERSION": '0.5.14',
            "ASCN_WGD": "WGD"
            },
        'Tumor2': {
            "purity": "0.36",
            "ploidy" : '7.9',
            "facets_version": '0.5.14',
            "genome_doubled": 'FALSE',
            "ASCN_PURITY": "0.36",
            "ASCN_PLOIDY": '7.9',
            "ASCN_VERSION": '0.5.14',
            "ASCN_WGD": "no WGD"
            }
        }
        sample_data =  {
                'TISSUE_SITE': '',
                'PROJECT_ID': '08390',
                'SAMPLE_COVERAGE': '108',
                'ONCOTREE_CODE': 'MEL',
                'IGO_ID': '08390_G_95',
                'PIPELINE': 'roslin',
                'SAMPLE_TYPE': 'Primary',
                'PATIENT_ID': 'Patient1',
                'SPECIMEN_PRESERVATION_TYPE': 'FFPE',
                'COLLAB_ID': 'Tumor-1',
                'GENE_PANEL': 'IMPACT468+08390_Hg19',
                'SAMPLE_ID': 'Tumor1',
                'REQUEST_ID': '08390_G',
                'PROJECT_PI': 'smithi',
                'PIPELINE_VERSION': '2.5.7',
                'REQUEST_PI': 'smithi',
                'SAMPLE_CLASS': 'Biopsy'
            }
        updated_sample_data = update_sample_data(sample_data, facets_data)
        expected_sample_data = {
            'TISSUE_SITE': '',
            'PROJECT_ID': '08390',
            'SAMPLE_COVERAGE': '108',
            'ONCOTREE_CODE': 'MEL',
            'IGO_ID': '08390_G_95',
            'PIPELINE': 'roslin',
            'SAMPLE_TYPE': 'Primary',
            'PATIENT_ID': 'Patient1',
            'SPECIMEN_PRESERVATION_TYPE': 'FFPE',
            'COLLAB_ID': 'Tumor-1',
            'GENE_PANEL': 'IMPACT468+08390_Hg19',
            'SAMPLE_ID': 'Tumor1',
            'REQUEST_ID': '08390_G',
            'PROJECT_PI': 'smithi',
            'PIPELINE_VERSION': '2.5.7',
            'REQUEST_PI': 'smithi',
            'SAMPLE_CLASS': 'Biopsy',
            "genome_doubled": 'TRUE',
            "ASCN_PURITY": "0.36",
            "ASCN_PLOIDY": '7.9',
            "ASCN_VERSION": '0.5.14',
            "ASCN_WGD": "WGD"
        }
        self.maxDiff = None
        self.assertDictEqual(updated_sample_data, expected_sample_data)

        sample_data =  {
            'TISSUE_SITE': '',
            'PROJECT_ID': '08390',
            'SAMPLE_COVERAGE': '502',
            'ONCOTREE_CODE': 'MEL',
            'IGO_ID': '08390_G_93',
            'PIPELINE': 'roslin',
            'SAMPLE_TYPE': 'Primary',
            'PATIENT_ID': 'Patient2',
            'SPECIMEN_PRESERVATION_TYPE': 'FFPE',
            'COLLAB_ID': 'Tumor-2',
            'GENE_PANEL': 'IMPACT468+08390_Hg19',
            'SAMPLE_ID': 'Tumor2',
            'REQUEST_ID': '08390_G',
            'PROJECT_PI': 'smithi',
            'PIPELINE_VERSION': '2.5.7',
            'REQUEST_PI': 'smithi',
            'SAMPLE_CLASS': 'Biopsy'
            }
        updated_sample_data = update_sample_data(sample_data, facets_data)
        expected_sample_data = {
            'TISSUE_SITE': '',
            'PROJECT_ID': '08390',
            'SAMPLE_COVERAGE': '502',
            'ONCOTREE_CODE': 'MEL',
            'IGO_ID': '08390_G_93',
            'PIPELINE': 'roslin',
            'SAMPLE_TYPE': 'Primary',
            'PATIENT_ID': 'Patient2',
            'SPECIMEN_PRESERVATION_TYPE': 'FFPE',
            'COLLAB_ID': 'Tumor-2',
            'GENE_PANEL': 'IMPACT468+08390_Hg19',
            'SAMPLE_ID': 'Tumor2',
            'REQUEST_ID': '08390_G',
            'PROJECT_PI': 'smithi',
            'PIPELINE_VERSION': '2.5.7',
            'REQUEST_PI': 'smithi',
            'SAMPLE_CLASS': 'Biopsy',
            "genome_doubled": 'FALSE',
            "ASCN_PURITY": "0.36",
            "ASCN_PLOIDY": '7.9',
            "ASCN_VERSION": '0.5.14',
            "ASCN_WGD": "no WGD"
        }
        self.assertDictEqual(updated_sample_data, expected_sample_data)

        # This one does not have a matching Facets data entry; should give NA values instead
        sample_data = {
            'TISSUE_SITE': '',
            'PROJECT_ID': '08390',
            'SAMPLE_COVERAGE': '500',
            'ONCOTREE_CODE': 'MEL',
            'IGO_ID': '08390_G_91',
            'PIPELINE': 'roslin',
            'SAMPLE_TYPE': 'Primary',
            'PATIENT_ID': 'Patient3',
            'SPECIMEN_PRESERVATION_TYPE': 'FFPE',
            'COLLAB_ID': 'Tumor-3',
            'GENE_PANEL': 'IMPACT468+08390_Hg19',
            'SAMPLE_ID': 'Tumor3',
            'REQUEST_ID': '08390_G',
            'PROJECT_PI': 'smithi',
            'PIPELINE_VERSION': '2.5.7',
            'REQUEST_PI': 'smithi',
            'SAMPLE_CLASS': 'Biopsy'
            }
        updated_sample_data = update_sample_data(sample_data, facets_data)
        expected_sample_data = {
            'TISSUE_SITE': '',
            'PROJECT_ID': '08390',
            'SAMPLE_COVERAGE': '500',
            'ONCOTREE_CODE': 'MEL',
            'IGO_ID': '08390_G_91',
            'PIPELINE': 'roslin',
            'SAMPLE_TYPE': 'Primary',
            'PATIENT_ID': 'Patient3',
            'SPECIMEN_PRESERVATION_TYPE': 'FFPE',
            'COLLAB_ID': 'Tumor-3',
            'GENE_PANEL': 'IMPACT468+08390_Hg19',
            'SAMPLE_ID': 'Tumor3',
            'REQUEST_ID': '08390_G',
            'PROJECT_PI': 'smithi',
            'PIPELINE_VERSION': '2.5.7',
            'REQUEST_PI': 'smithi',
            'SAMPLE_CLASS': 'Biopsy',
            "genome_doubled": 'NA',
            "ASCN_PURITY": "NA",
            "ASCN_PLOIDY": 'NA',
            "ASCN_VERSION": 'NA',
            "ASCN_WGD": "NA"
        }
        self.assertDictEqual(updated_sample_data, expected_sample_data)


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
