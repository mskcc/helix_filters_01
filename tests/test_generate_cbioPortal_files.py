#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for the generation of cBio Portal files
"""
import sys
import os
import csv
import json
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
from bin.generate_cbioPortal_files import load_clinical_data, load_sample_coverages, header_lines_map
from bin.generate_cbioPortal_files import generate_portal_data_clinical_patient
from bin.generate_cbioPortal_files import generate_portal_data_clinical_sample
from bin.generate_cbioPortal_files import generate_header_lines
from bin.generate_cbioPortal_files import create_file_lines
sys.path.pop(0)



class TestGenerateCBioFiles(unittest.TestCase):
    def test_get_inputs(self):
        """
        """
        data_clinical_file = os.path.join(DATA_SETS['Proj_08390_G']['INPUTS_DIR'], "Proj_08390_G_sample_data_clinical.txt")
        clinical_data = load_clinical_data(data_clinical_file)
        # clinical_data is OrderedDict; keys:
        #  1	SAMPLE_ID
        #  2	IGO_ID
        #  3	PATIENT_ID
        #  4	COLLAB_ID
        #  5	SAMPLE_TYPE
        #  6	SAMPLE_CLASS
        #  7	GENE_PANEL
        #  8	ONCOTREE_CODE
        #  9	SPECIMEN_PRESERVATION_TYPE
        # 10	SEX
        # 11	TISSUE_SITE
        # 12	REQUEST_ID
        # 13	PROJECT_ID
        # 14	PIPELINE
        # 15	PIPELINE_VERSION

        sample_summary_file = os.path.join(DATA_SETS['Proj_08390_G']['QC_DIR'], "Proj_08390_G_SampleSummary.txt")
        sample_coverages = load_sample_coverages(sample_summary_file)

        for row in clinical_data:
            # add the matching coverages to the clincal data, or a '' empty value
            row['SAMPLE_COVERAGE'] = sample_coverages.get(row['SAMPLE_ID'], '')
        #     # move SAMPLE_ID and PATIENT_ID to the front
        #     row.move_to_end()
        #
        # for item in clinical_data:
        #     print(item)
        # # x.move_to_end('a', last = False)


    def test_generate_portal_data_clinical_patient(self):
        """
        Test that clinical patient data is generated correctly
        it should be a subset of the expected dict keys
        """
        clinical_data = [
        {'PATIENT_ID': 'Patient1', 'SEX': 'M', 'foo': 'bar', 'baz': 'buzz'},
        {'PATIENT_ID': 'Patient2', 'SEX': 'F', 'foo': 'bar1', 'baz': 'buzz1'}
        ]
        clinical_patient_data = generate_portal_data_clinical_patient(clinical_data)
        expected_data = [
        {'PATIENT_ID': 'Patient1', 'SEX': 'M'},
        {'PATIENT_ID': 'Patient2', 'SEX': 'F'}
        ]
        self.assertEqual(clinical_patient_data, expected_data)

    def test_generate_portal_data_clinical_sample(self):
        """
        Test that clinical patient data is generated correctly
        it should be a subset of the expected dict keys
        """
        clinical_data = [
            {
            "SAMPLE_ID": "Sample1",
            "PATIENT_ID": "Patient1",
            "TISSUE_SITE": "Lung",
            "SAMPLE_COVERAGE": "1",
            "ONCOTREE_CODE": "ABC",
            "IGO_ID": "IGO_1",
            "PIPELINE": "roslin",
            "SAMPLE_TYPE": "Adenocarcinoma",
            "COLLAB_ID": "Collab_1",
            "GENE_PANEL": "IMPACT468",
            "REQUEST_ID": "Request_1",
            "SPECIMEN_PRESERVATION_TYPE": "FFPE",
            "PIPELINE_VERSION": "1",
            "PROJECT_ID": "Project_1",
            "SAMPLE_CLASS": "Biopsy",
            "PROJECT_PI": "PI Bob",
            "REQUEST_PI": "PI Jones",
            "foo": "bar",
            "buz": "baz"
            }
        ]
        clinical_sample_data = generate_portal_data_clinical_sample(clinical_data)
        expected_data = [
            {
            "SAMPLE_ID": "Sample1",
            "PATIENT_ID": "Patient1",
            "TISSUE_SITE": "Lung",
            "SAMPLE_COVERAGE": "1",
            "ONCOTREE_CODE": "ABC",
            "IGO_ID": "IGO_1",
            "PIPELINE": "roslin",
            "SAMPLE_TYPE": "Adenocarcinoma",
            "COLLAB_ID": "Collab_1",
            "GENE_PANEL": "IMPACT468",
            "REQUEST_ID": "Request_1",
            "SPECIMEN_PRESERVATION_TYPE": "FFPE",
            "PIPELINE_VERSION": "1",
            "PROJECT_ID": "Project_1",
            "SAMPLE_CLASS": "Biopsy",
            "PROJECT_PI": "PI Bob",
            "REQUEST_PI": "PI Jones",
            }
        ]
        self.assertEqual(clinical_sample_data, expected_data)


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
        '#SAMPLE_ID\tIGO_ID\tPATIENT_ID\tSAMPLE_TYPE\tSAMPLE_CLASS\tGENE_PANEL\tONCOTREE_CODE\tSPECIMEN_PRESERVATION_TYPE\tSEX\tTISSUE_SITE\tREQUEST_ID\tPROJECT_ID\tPIPELINE\tPIPELINE_VERSION',
        '#SAMPLE_ID\tIGO_ID\tPATIENT_ID\tSAMPLE_TYPE\tSAMPLE_CLASS\tGENE_PANEL\tONCOTREE_CODE\tSPECIMEN_PRESERVATION_TYPE\tSEX\tTISSUE_SITE\tREQUEST_ID\tPROJECT_ID\tPIPELINE\tPIPELINE_VERSION',
        '#STRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING',
        '#1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1'
        ]
        self.assertEqual(header_lines, expected_lines)

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
        '#PATIENT_ID\tSEX',
        '#PATIENT_ID\tSEX',
        '#STRING\tSTRING',
        '#1\t1',
        'PATIENT_ID\tSEX',
        'Patient1\tM',
        'Patient2\tF'
        ]
        self.assertEqual(lines, expected_lines)


if __name__ == "__main__":
    unittest.main()
