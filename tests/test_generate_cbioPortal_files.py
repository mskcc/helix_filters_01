#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for the generation of cBio Portal files
"""
import sys
import os
import unittest

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from pluto.tools import PlutoTestCase
from pluto.settings import DATA_SETS
from settings import BIN_DIR
from bin.generate_cbioPortal_files import generate_portal_data_clinical_patient
from bin.generate_cbioPortal_files import generate_portal_data_clinical_sample
from bin.generate_cbioPortal_files import generate_study_meta
from bin.generate_cbioPortal_files import generate_extra_group_labels_string
from bin.generate_cbioPortal_files import generate_meta_lines
from bin.generate_cbioPortal_files import generate_clinical_meta_samples_data
from bin.generate_cbioPortal_files import generate_clinical_meta_patient_data
from bin.generate_cbioPortal_files import generate_clinical_meta_cna_data
from bin.generate_cbioPortal_files import generate_fusion_meta_data
from bin.generate_cbioPortal_files import generate_mutation_meta_data
from bin.generate_cbioPortal_files import generate_case_list_all_data
from bin.generate_cbioPortal_files import generate_case_list_cnaseq_data
from bin.generate_cbioPortal_files import generate_case_list_cna_data
from bin.generate_cbioPortal_files import generate_case_list_sequenced_data
from bin.generate_cbioPortal_files import get_sample_list
from bin.generate_cbioPortal_files import generate_meta_segments_data
from bin.generate_cbioPortal_files import generate_data_clinical_sample_file
from bin.generate_cbioPortal_files import clean_facets_suite_cna_file
sys.path.pop(0)

class TestGenerateCBioFiles(PlutoTestCase):
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

    def test_generate_portal_data_clinical_patient_dupes(self):
        """
        Test that clinical patient data is generated correctly
        There should be no duplicate PATIENT_ID's in the output even if the input has duplicates
        """
        clinical_data = [
        {'PATIENT_ID': 'Patient1', 'SEX': 'M', 'foo': 'bar', 'baz': 'buzz'},
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

    def test_generate_data_clinical_sample_file_with_facets_and_summary(self):
        """
        generate_data_clinical_sample_file
        """
        self.maxDiff = None
        data_clinical_file = os.path.join(DATA_SETS['Proj_08390_G']['INPUTS_DIR'], 'Proj_08390_G_sample_data_clinical.1.txt')
        sample_summary_file = os.path.join(DATA_SETS['Proj_08390_G']['QC_DIR'], 'Proj_08390_G_SampleSummary.txt')
        facets_txt_file = os.path.join(DATA_SETS['Proj_08390_G']['FACETS_SUITE_DIR'], 'Proj_08390_G.facets.txt')

        output_file = os.path.join(self.tmpdir, "output.txt")
        args = {
        'data_clinical_file': data_clinical_file,
        'sample_summary_file': sample_summary_file,
        'facets_txt_files': [facets_txt_file],
        'output': output_file,
        'project_pi': 'jonesd',
        'request_pi': 'smithd'
        }
        generate_data_clinical_sample_file(**args)
        with open(output_file) as fin:
            lines = [ line.strip().split('\t') for line in fin ]

        expected_lines = [
        ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'SAMPLE_COVERAGE', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
        ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'SAMPLE_COVERAGE', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
        ['#STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'NUMBER', 'STRING', 'STRING', 'STRING', 'NUMBER', 'NUMBER', 'STRING', 'STRING'],
        ['#1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '0', '1'],
        ['SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'SAMPLE_COVERAGE', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
        ['Sample46', '08390_G_95', 'p_C_00001', 'COLLAB-01-T', 'Primary', 'Biopsy', 'IMPACT468+08390_Hg19', 'MEL', 'FFPE', '', '08390_G', '08390', 'roslin', '2.5.7', '108', 'jonesd', 'smithd', 'FALSE', '0.36', '2.6', '0.5.14', 'no WGD']
        ]

        self.assertEqual(lines, expected_lines)

    def test_generate_data_clinical_sample_file_with_facets(self):
        """
        Test that we can generate correct data clinical sample file a facets txt file is provided
        """
        self.maxDiff = None

        data_clinical_file = os.path.join(DATA_SETS['Proj_08390_G']['INPUTS_DIR'], 'Proj_08390_G_sample_data_clinical.1.txt')
        facets_txt_file = os.path.join(DATA_SETS['Proj_08390_G']['FACETS_SUITE_DIR'], 'Proj_08390_G.facets.txt')
        output_file = os.path.join(self.tmpdir, "output.txt")
        args = {
        'data_clinical_file': data_clinical_file,
        'sample_summary_file': None,
        'facets_txt_files': [facets_txt_file],
        'output': output_file,
        'project_pi': 'jonesd',
        'request_pi': 'smithd'
        }
        generate_data_clinical_sample_file(**args)
        with open(output_file) as fin:
            lines = [ line.strip().split('\t') for line in fin ]

        expected_lines = [
        ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
        ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
        ['#STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'NUMBER', 'NUMBER', 'STRING', 'STRING'],
        ['#1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '0', '1'],
        ['SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
        ['Sample46', '08390_G_95', 'p_C_00001', 'COLLAB-01-T', 'Primary', 'Biopsy', 'IMPACT468+08390_Hg19', 'MEL', 'FFPE', '', '08390_G', '08390', 'roslin', '2.5.7', 'jonesd', 'smithd', 'FALSE', '0.36', '2.6', '0.5.14', 'no WGD']
        ]

        self.assertEqual(lines, expected_lines)

    def test_generate_data_clinical_sample_file_with_two_facets(self):
        """
        Test that we can generate correct data clinical sample file when multiple facets txt files are provided
        """
        # file for Sample46 and Sample44
        data_clinical_file = os.path.join(DATA_SETS['Proj_08390_G']['INPUTS_DIR'], 'Proj_08390_G_sample_data_clinical.2.txt')
        facets_txt_file1 = os.path.join(DATA_SETS['Proj_08390_G']['FACETS_SUITE_DIR'], 'Sample46.txt')
        facets_txt_file2 = os.path.join(DATA_SETS['Proj_08390_G']['FACETS_SUITE_DIR'], 'Sample44.txt')

        output_file = os.path.join(self.tmpdir, "output.txt")
        args = {
        'data_clinical_file': data_clinical_file,
        'sample_summary_file': None,
        'facets_txt_files': [facets_txt_file1, facets_txt_file2],
        'output': output_file,
        'project_pi': 'jonesd',
        'request_pi': 'smithd'
        }
        generate_data_clinical_sample_file(**args)
        with open(output_file) as fin:
            lines = [ line.strip().split('\t') for line in fin ]

        expected_lines = [
            ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
            ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
            ['#STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'NUMBER', 'NUMBER', 'STRING', 'STRING'],
            ['#1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '0', '1'],
            ['SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
            ['Sample46', '08390_G_95', 'p_C_00001', 'COLLAB-01-T', 'Primary', 'Biopsy', 'IMPACT468+08390_Hg19', 'MEL', 'FFPE', '', '08390_G', '08390', 'roslin', '2.5.7', 'jonesd', 'smithd', 'FALSE', '0.36', '2.6', '0.5.14', 'no WGD'],
            ['Sample44', '08390_G_93', 'p_C_00002', 'COLLAB-01-T', 'Primary', 'Biopsy', 'IMPACT468+08390_Hg19', 'MEL', 'FFPE', '', '08390_G', '08390', 'roslin', '2.5.7', 'jonesd', 'smithd', 'FALSE', '0.51', '1.6', '0.5.14', 'no WGD']
            ]

        self.assertEqual(lines, expected_lines)


    def test_generate_data_clinical_sample_file_mismatched_facets(self):
        """
        Test that some Facets data can be correctly loaded when provided Facets files do not match all samples in the data clinical file
        """
        data_clinical_file = os.path.join(DATA_SETS['Proj_08390_G']['INPUTS_DIR'], 'Proj_08390_G_sample_data_clinical.2.txt')
        facets_txt_file1 = os.path.join(DATA_SETS['Proj_08390_G']['FACETS_SUITE_DIR'], 'Sample46.txt')
        facets_txt_file2 = os.path.join(DATA_SETS['Proj_08390_G']['FACETS_SUITE_DIR'], 'Sample1.txt')

        output_file = os.path.join(self.tmpdir, "output.txt")
        args = {
        'data_clinical_file': data_clinical_file,
        'sample_summary_file': None,
        'facets_txt_files': [facets_txt_file1, facets_txt_file2],
        'output': output_file,
        'project_pi': 'jonesd',
        'request_pi': 'smithd'
        }
        generate_data_clinical_sample_file(**args)
        with open(output_file) as fin:
            lines = [ line.strip().split('\t') for line in fin ]

        expected_lines = [
            ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
            ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
            ['#STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'NUMBER', 'NUMBER', 'STRING', 'STRING'],
            ['#1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '0', '1'],
            ['SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
            ['Sample46', '08390_G_95', 'p_C_00001', 'COLLAB-01-T', 'Primary', 'Biopsy', 'IMPACT468+08390_Hg19', 'MEL', 'FFPE', '', '08390_G', '08390', 'roslin', '2.5.7', 'jonesd', 'smithd', 'FALSE', '0.36', '2.6', '0.5.14', 'no WGD'],
            ['Sample44', '08390_G_93', 'p_C_00002', 'COLLAB-01-T', 'Primary', 'Biopsy', 'IMPACT468+08390_Hg19', 'MEL', 'FFPE', '', '08390_G', '08390', 'roslin', '2.5.7', 'jonesd', 'smithd', 'NA', 'NA', 'NA', 'NA', 'NA']
            ]

        self.assertEqual(lines, expected_lines)



    def test_test_generate_data_clinical_sample_file_mismatched_facets_cli(self):
        """
        Test that some Facets data can be correctly loaded when provided Facets files do not match all samples in the data clinical file
        Using command line invocation
        """
        data_clinical_file = os.path.join(DATA_SETS['Proj_08390_G']['INPUTS_DIR'], 'Proj_08390_G_sample_data_clinical.2.txt')
        facets_txt_file1 = os.path.join(DATA_SETS['Proj_08390_G']['FACETS_SUITE_DIR'], 'Sample46.txt')
        facets_txt_file2 = os.path.join(DATA_SETS['Proj_08390_G']['FACETS_SUITE_DIR'], 'Sample44.txt')

        script = os.path.join(BIN_DIR, 'generate_cbioPortal_files.py')

        output_file = os.path.join(self.tmpdir, "output.txt")

        command = [
        script,
        'sample',
        '--output', output_file,
        '--data-clinical-file', data_clinical_file,
        '--project-pi', 'jonesd',
        '--request-pi', 'smithd',
        '--facets-txt-files', facets_txt_file1, facets_txt_file2
        ]

        returncode, proc_stdout, proc_stderr = self.run_command(command)

        if returncode != 0:
            print(proc_stderr)

        self.assertEqual(returncode, 0)

        with open(output_file) as fin:
            lines = [ line.strip().split('\t') for line in fin ]

        expected_lines = [
            ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
            ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
            ['#STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'NUMBER', 'NUMBER', 'STRING', 'STRING'],
            ['#1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '0', '1'],
            ['SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI', 'genome_doubled', 'ASCN_PURITY', 'ASCN_PLOIDY', 'ASCN_VERSION', 'ASCN_WGD'],
            ['Sample46', '08390_G_95', 'p_C_00001', 'COLLAB-01-T', 'Primary', 'Biopsy', 'IMPACT468+08390_Hg19', 'MEL', 'FFPE', '', '08390_G', '08390', 'roslin', '2.5.7', 'jonesd', 'smithd', 'FALSE', '0.36', '2.6', '0.5.14', 'no WGD'],
            ['Sample44', '08390_G_93', 'p_C_00002', 'COLLAB-01-T', 'Primary', 'Biopsy', 'IMPACT468+08390_Hg19', 'MEL', 'FFPE', '', '08390_G', '08390', 'roslin', '2.5.7', 'jonesd', 'smithd', 'FALSE', '0.51', '1.6', '0.5.14', 'no WGD']
            ]

        self.assertEqual(lines, expected_lines)

    def test_generate_data_clinical_sample_file_with_summary(self):
        """
        generate_data_clinical_sample_file
        """
        self.maxDiff = None

        data_clinical_file = os.path.join(DATA_SETS['Proj_08390_G']['INPUTS_DIR'], 'Proj_08390_G_sample_data_clinical.1.txt')
        sample_summary_file = os.path.join(DATA_SETS['Proj_08390_G']['QC_DIR'], 'Proj_08390_G_SampleSummary.txt')
        output_file = os.path.join(self.tmpdir, "output.txt")
        args = {
        'data_clinical_file': data_clinical_file,
        'sample_summary_file': sample_summary_file,
        'output': output_file,
        'project_pi': 'jonesd',
        'request_pi': 'smithd'
        }
        generate_data_clinical_sample_file(**args)
        with open(output_file) as fin:
            lines = [ line.strip().split('\t') for line in fin ]

        expected_lines = [
        ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'SAMPLE_COVERAGE', 'PROJECT_PI', 'REQUEST_PI'],
        ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'SAMPLE_COVERAGE', 'PROJECT_PI', 'REQUEST_PI'],
        ['#STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'NUMBER', 'STRING', 'STRING'],
        ['#1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'SAMPLE_COVERAGE', 'PROJECT_PI', 'REQUEST_PI'],
        ['Sample46', '08390_G_95', 'p_C_00001', 'COLLAB-01-T', 'Primary', 'Biopsy', 'IMPACT468+08390_Hg19', 'MEL', 'FFPE', '', '08390_G', '08390', 'roslin', '2.5.7', '108', 'jonesd', 'smithd']
        ]

        self.assertEqual(lines, expected_lines)

    def test_generate_data_clinical_sample_file(self):
        """
        generate_data_clinical_sample_file
        """
        self.maxDiff = None

        data_clinical_file = os.path.join(DATA_SETS['Proj_08390_G']['INPUTS_DIR'], 'Proj_08390_G_sample_data_clinical.1.txt')
        output_file = os.path.join(self.tmpdir, "output.txt")
        args = {
        'data_clinical_file': data_clinical_file,
        'sample_summary_file': None,
        'output': output_file,
        'project_pi': 'jonesd',
        'request_pi': 'smithd'
        }
        generate_data_clinical_sample_file(**args)
        with open(output_file) as fin:
            lines = [ line.strip().split('\t') for line in fin ]

        expected_lines = [
        ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI'],
        ['#SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI'],
        ['#STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING', 'STRING'],
        ['#1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
        ['SAMPLE_ID', 'IGO_ID', 'PATIENT_ID', 'COLLAB_ID', 'SAMPLE_TYPE', 'SAMPLE_CLASS', 'GENE_PANEL', 'ONCOTREE_CODE', 'SPECIMEN_PRESERVATION_TYPE', 'TISSUE_SITE', 'REQUEST_ID', 'PROJECT_ID', 'PIPELINE', 'PIPELINE_VERSION', 'PROJECT_PI', 'REQUEST_PI'], ['Sample46', '08390_G_95', 'p_C_00001', 'COLLAB-01-T', 'Primary', 'Biopsy', 'IMPACT468+08390_Hg19', 'MEL', 'FFPE', '', '08390_G', '08390', 'roslin', '2.5.7', 'jonesd', 'smithd']
        ]

        self.assertEqual(lines, expected_lines)

    def test_generate_study_meta(self):
        """
        """
        data = generate_study_meta(
            cancer_study_identifier = "identifier",
            description = "description",
            name = 'name',
            short_name = 'short_name',
            type_of_cancer = "type_of_cancer"
        )
        expected_data = {
        'cancer_study_identifier' : 'identifier',
        'description': 'description',
        'groups': 'PRISM;COMPONC;VIALEA',
        'name': 'name',
        'short_name': 'short_name',
        'type_of_cancer': 'type_of_cancer'
        }
        self.assertEqual(data, expected_data)

        data = generate_study_meta(
            cancer_study_identifier = "identifier",
            description = "description",
            name = 'name',
            short_name = 'short_name',
            extra_groups = ["extra_group1", "extra_group2"],
            type_of_cancer = "type_of_cancer"
        )
        expected_data = {
        'cancer_study_identifier' : 'identifier',
        'description': 'description',
        'groups': 'PRISM;COMPONC;VIALEA;EXTRA_GROUP1;EXTRA_GROUP2',
        'name': 'name',
        'short_name': 'short_name',
        'type_of_cancer': 'type_of_cancer'
        }
        self.assertEqual(data, expected_data)

        data = generate_study_meta(
            cancer_study_identifier = "identifier",
            description = "description\ndescription\ndescription",
            name = 'name',
            short_name = 'short_name',
            extra_groups = ["extra_group1", "extra_group2"],
            type_of_cancer = "type_of_cancer"
        )
        expected_data = {
        'cancer_study_identifier' : 'identifier',
        'description': 'descriptiondescriptiondescription',
        'groups': 'PRISM;COMPONC;VIALEA;EXTRA_GROUP1;EXTRA_GROUP2',
        'name': 'name',
        'short_name': 'short_name',
        'type_of_cancer': 'type_of_cancer'
        }
        self.assertEqual(data, expected_data)

    def test_generate_extra_group_labels_string(self):
        """
        Test that extra group labels are converted into a label string correctly
        """
        extra_groups = []
        groups_str = generate_extra_group_labels_string(extra_groups)
        expected_str = ''
        self.assertEqual(groups_str, expected_str)

        extra_groups = ['foo']
        groups_str = generate_extra_group_labels_string(extra_groups)
        expected_str = 'FOO'
        self.assertEqual(groups_str, expected_str)

        extra_groups = ['foo', 'bar']
        groups_str = generate_extra_group_labels_string(extra_groups)
        expected_str = 'FOO;BAR'
        self.assertEqual(groups_str, expected_str)

        extra_groups = ['foo', 'na']
        groups_str = generate_extra_group_labels_string(extra_groups)
        expected_str = 'FOO'
        self.assertEqual(groups_str, expected_str)

        extra_groups = ['foo', 'na', 'pitt', 'bar']
        groups_str = generate_extra_group_labels_string(extra_groups)
        expected_str = 'FOO;BAR'
        self.assertEqual(groups_str, expected_str)

        extra_groups = ['foo   bar']
        groups_str = generate_extra_group_labels_string(extra_groups)
        expected_str = 'FOOBAR'
        self.assertEqual(groups_str, expected_str)

    def test_generate_meta_lines(self):
        """
        Test that lines for metadata files are generated correctly based on a given dict
        """
        data = {
        'foo': 'bar',
        'baz': 'buzz'
        }
        lines = generate_meta_lines(data)
        expected_lines = [
        'foo: bar\n',
        'baz: buzz\n'
        ]
        self.assertEqual(lines, expected_lines)


    def test_generate_clinical_meta_samples_data(self):
        """
        """
        data = generate_clinical_meta_samples_data(cancer_study_identifier = "foo", data_filename = "bar.txt")
        expected_data = {
        'cancer_study_identifier': "foo",
        'data_filename': 'bar.txt',
        'datatype': 'SAMPLE_ATTRIBUTES',
        'genetic_alteration_type': 'CLINICAL'
        }
        self.assertDictEqual(data, expected_data)

    def test_generate_clinical_meta_patient_data(self):
        """
        """
        data = generate_clinical_meta_patient_data(cancer_study_identifier = "foo", data_filename = "bar.txt")
        expected_data = {
        'cancer_study_identifier': "foo",
        'data_filename': 'bar.txt',
        'datatype': 'PATIENT_ATTRIBUTES',
        'genetic_alteration_type': 'CLINICAL'
        }
        self.assertDictEqual(data, expected_data)

    def test_generate_clinical_meta_cna_data(self):
        """
        """
        data = generate_clinical_meta_cna_data(cancer_study_identifier = "foo", data_filename = "bar.txt")
        expected_data = {
        'cancer_study_identifier': "foo",
        'data_filename': 'bar.txt',
        'datatype': 'DISCRETE',
        'genetic_alteration_type': 'COPY_NUMBER_ALTERATION',
        'stable_id': 'cna',
        'show_profile_in_analysis_tab': 'true',
        'profile_name': 'Discrete Copy Number Data',
        'profile_description': 'Discrete Copy Number Data'
        }
        self.assertDictEqual(data, expected_data)

    def test_generate_fusion_meta_data(self):
        """
        """
        data = generate_fusion_meta_data(cancer_study_identifier = "foo", data_filename = "bar.txt")
        expected_data = {
        'cancer_study_identifier': "foo",
        'data_filename': 'bar.txt',
        'genetic_alteration_type': 'FUSION',
        'stable_id': 'fusion',
        'show_profile_in_analysis_tab': 'true',
        'profile_name': 'Fusions',
        'profile_description': 'Fusion data',
        'datatype': 'FUSION'
        }
        self.assertDictEqual(data, expected_data)

    def test_generate_mutation_meta_data(self):
        """
        """
        data = generate_mutation_meta_data(cancer_study_identifier = "foo", data_filename = "bar.txt")
        expected_data = {
        'cancer_study_identifier': 'foo',
        'data_filename': 'bar.txt',
        'genetic_alteration_type': 'MUTATION_EXTENDED',
        'datatype': 'MAF',
        'stable_id': 'mutations',
        'show_profile_in_analysis_tab': "true",
        'profile_description': 'Mutation data',
        'profile_name': 'Mutations'
        }
        self.assertDictEqual(data, expected_data)

    def test_generate_case_list_all_data(self):
        """
        """
        data = generate_case_list_all_data(cancer_study_identifier = "foo", case_list_ids = ['bar', 'baz', 'buzz'])
        expected_data = {
        'cancer_study_identifier': 'foo',
        'stable_id': 'foo_all',
        'case_list_category': 'all_cases_in_study',
        'case_list_name': 'All Tumors',
        'case_list_description': 'All tumor samples',
        'case_list_ids': 'bar\tbaz\tbuzz'
        }
        self.assertDictEqual(data, expected_data)

    def test_generate_case_list_cnaseq_data(self):
        """
        """
        data = generate_case_list_cnaseq_data(cancer_study_identifier = "foo", case_list_ids = ['bar', 'baz', 'buzz'])
        expected_data = {
        'cancer_study_identifier': 'foo',
        'stable_id': 'foo_cnaseq',
        'case_list_category': 'all_cases_with_mutation_and_cna_data',
        'case_list_name': 'Tumors with sequencing and CNA data',
        'case_list_description': 'All tumor samples that have CNA and sequencing data',
        'case_list_ids': 'bar\tbaz\tbuzz'
        }
        self.assertDictEqual(data, expected_data)

    def test_generate_case_list_cna_data(self):
        """
        """
        data = generate_case_list_cna_data(cancer_study_identifier = "foo", case_list_ids = ['bar', 'baz', 'buzz'])
        expected_data = {
        'cancer_study_identifier': 'foo',
        'stable_id': 'foo_cna',
        'case_list_category': 'all_cases_with_cna_data',
        'case_list_name': 'Tumors CNA',
        'case_list_description': 'All tumors with CNA data',
        'case_list_ids': 'bar\tbaz\tbuzz'
        }
        self.assertDictEqual(data, expected_data)

    def test_generate_case_list_sequenced_data(self):
        """
        """
        data = generate_case_list_sequenced_data(cancer_study_identifier = "foo", case_list_ids = ['bar', 'baz', 'buzz'])
        expected_data = {
        'cancer_study_identifier': 'foo',
        'stable_id': 'foo_sequenced',
        'case_list_category': 'all_cases_with_mutation_data',
        'case_list_name': 'Sequenced Tumors',
        'case_list_description': 'All sequenced tumors',
        'case_list_ids': 'bar\tbaz\tbuzz'
        }
        self.assertDictEqual(data, expected_data)

    def test_get_sample_list(self):
        """
        """
        clinical_data = [
        {'SAMPLE_ID': 'foo1', 'bar': 'buzz'},
        {'SAMPLE_ID': 'foo2', 'bar': 'buzz'},
        {'SAMPLE_ID': 'foo3', 'bar': 'buzz'}
        ]
        sample_list = get_sample_list(clinical_data)
        expected_list = ['foo1', 'foo2', 'foo3']
        self.assertEqual(sample_list, expected_list)

    def test_generate_meta_segments_data(self):
        """
        """
        data = generate_meta_segments_data(cancer_study_identifier = "foo", data_filename = "bar.txt")
        expected_data = {
        'cancer_study_identifier': 'foo',
        'data_filename': 'bar.txt',
        'genetic_alteration_type': 'COPY_NUMBER_ALTERATION',
        'datatype': 'SEG',
        'description': 'Segmented Data',
        'reference_genome_id': 'hg19'
        }
        self.assertDictEqual(data, expected_data)

    def test_clean_facets_suite_cna_data(self):
        """
        Some files output by Facets Suite have '_hisens' appended to the sample IDs, need to test that this gets detected and removed

        affected files;

        portal/data_CNA.txt
        portal/data_CNA.ascna.txt
        """
        # test case with clean headers
        cna_lines = [
        ['Hugo_Symbol', 'sample1', 'sample2'],
        ['ABL1', '3;1', '3;NA']
        ]
        input_file = self.write_table(self.tmpdir, "data_CNA.txt", cna_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        clean_facets_suite_cna_file(input_file = input_file, output_file = output_file)
        with open(output_file) as fin:
            lines = [ l for l in fin ]
        expected_lines = ['Hugo_Symbol\tsample1\tsample2\n', 'ABL1\t3;1\t3;NA\n']
        self.assertEqual(lines, expected_lines)

        # test case with bad headers
        cna_lines = [
        ['Hugo_Symbol', 'sample1_hisens', 'sample2_hisens'],
        ['ABL1', '3;1', '3;NA']
        ]
        input_file = self.write_table(self.tmpdir, "data_CNA.txt", cna_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        clean_facets_suite_cna_file(input_file = input_file, output_file = output_file)
        with open(output_file) as fin:
            lines = [ l for l in fin ]
        expected_lines = ['Hugo_Symbol\tsample1\tsample2\n', 'ABL1\t3;1\t3;NA\n']
        self.assertEqual(lines, expected_lines)

        # test case with mixed headers
        cna_lines = [
        ['Hugo_Symbol', 'sample1', 'sample2_hisens'],
        ['ABL1', '3;1', '3;NA']
        ]
        input_file = self.write_table(self.tmpdir, "data_CNA.txt", cna_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        clean_facets_suite_cna_file(input_file = input_file, output_file = output_file)
        with open(output_file) as fin:
            lines = [ l for l in fin ]
        expected_lines = ['Hugo_Symbol\tsample1\tsample2\n', 'ABL1\t3;1\t3;NA\n']
        self.assertEqual(lines, expected_lines)

        # run it from the command line
        script = os.path.join(BIN_DIR, 'generate_cbioPortal_files.py')
        cna_lines = [
        ['Hugo_Symbol', 'sample1', 'sample2_hisens'],
        ['ABL1', '3;1', '3;NA']
        ]
        input_file = self.write_table(self.tmpdir, "data_CNA.txt", cna_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")

        command = [
        script,
        'clean_cna',
        '--output', output_file,
        '--input', input_file
        ]

        returncode, proc_stdout, proc_stderr = self.run_command(command)

        if returncode != 0:
            print(proc_stderr)

        self.assertEqual(returncode, 0)

        with open(output_file) as fin:
            lines = [ l for l in fin ]
        expected_lines = ['Hugo_Symbol\tsample1\tsample2\n', 'ABL1\t3;1\t3;NA\n']
        self.assertEqual(lines, expected_lines)






if __name__ == "__main__":
    unittest.main()
