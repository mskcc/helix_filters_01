#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for cBioPortal utility functions
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
from bin.cBioPortal_utils import create_file_lines
from bin.cBioPortal_utils import generate_header_lines
from bin.cBioPortal_utils import update_sample_data
from bin.cBioPortal_utils import parse_facets_data
sys.path.pop(0)

class TestCBioUtils(unittest.TestCase):
    def test_create_file_lines(self):
        """
        Test that all the lines for a set of data are created correctly
        """
        clinical_data = [
        {'PATIENT_ID': 'Patient1', 'SEX': 'M'},
        {'PATIENT_ID': 'Patient2', 'SEX': 'F'}
        ]
        lines = create_file_lines(clinical_data)
        expected_lines = [
        '#PATIENT_ID\tSEX\n',
        '#PATIENT_ID\tSEX\n',
        '#STRING\tSTRING\n',
        '#1\t1\n',
        'PATIENT_ID\tSEX\n',
        'Patient1\tM\n',
        'Patient2\tF\n'
        ]
        self.assertEqual(lines, expected_lines)

    def test_generate_header_lines(self):
        """
        Test that the header lines are generated as expected for the given column headers
        """
        keys = [
        'SAMPLE_ID',
        'IGO_ID',
        'PATIENT_ID',
        'SAMPLE_TYPE',
        'SAMPLE_CLASS',
        'GENE_PANEL',
        'ONCOTREE_CODE',
        'SPECIMEN_PRESERVATION_TYPE',
        'SEX',
        'TISSUE_SITE',
        'REQUEST_ID',
        'PROJECT_ID',
        'PIPELINE',
        'PIPELINE_VERSION'
        ]
        header_lines = generate_header_lines(keys)
        expected_lines = [
        '#SAMPLE_ID\tIGO_ID\tPATIENT_ID\tSAMPLE_TYPE\tSAMPLE_CLASS\tGENE_PANEL\tONCOTREE_CODE\tSPECIMEN_PRESERVATION_TYPE\tSEX\tTISSUE_SITE\tREQUEST_ID\tPROJECT_ID\tPIPELINE\tPIPELINE_VERSION\n',
        '#SAMPLE_ID\tIGO_ID\tPATIENT_ID\tSAMPLE_TYPE\tSAMPLE_CLASS\tGENE_PANEL\tONCOTREE_CODE\tSPECIMEN_PRESERVATION_TYPE\tSEX\tTISSUE_SITE\tREQUEST_ID\tPROJECT_ID\tPIPELINE\tPIPELINE_VERSION\n',
        '#STRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\n',
        '#1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\n'
        ]
        self.assertEqual(header_lines, expected_lines)


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



if __name__ == "__main__":
    unittest.main()