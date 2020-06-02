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
        '#SAMPLE_ID\tIGO_ID\tPATIENT_ID\tSAMPLE_TYPE\tSAMPLE_CLASS\tGENE_PANEL\tONCOTREE_CODE\tSPECIMEN_PRESERVATION_TYPE\tSEX\tTISSUE_SITE\tREQUEST_ID\tPROJECT_ID\tPIPELINE\tPIPELINE_VERSION\n',
        '#SAMPLE_ID\tIGO_ID\tPATIENT_ID\tSAMPLE_TYPE\tSAMPLE_CLASS\tGENE_PANEL\tONCOTREE_CODE\tSPECIMEN_PRESERVATION_TYPE\tSEX\tTISSUE_SITE\tREQUEST_ID\tPROJECT_ID\tPIPELINE\tPIPELINE_VERSION\n',
        '#STRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\tSTRING\n',
        '#1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\t1\n'
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
        '#PATIENT_ID\tSEX\n',
        '#PATIENT_ID\tSEX\n',
        '#STRING\tSTRING\n',
        '#1\t1\n',
        'PATIENT_ID\tSEX\n',
        'Patient1\tM\n',
        'Patient2\tF\n'
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
        'stable_id': 'foo_all',
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
        'stable_id': 'foo_all',
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
        'stable_id': 'foo_all',
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





if __name__ == "__main__":
    unittest.main()
