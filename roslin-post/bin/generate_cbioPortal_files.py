#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

ported over from roslin_analysis_helper.py
need functions:

generate_legacy_clinical_data
get_sample_list
create_case_list_file
generate_case_lists
generate_study_meta
generate_segmented_meta
generate_discrete_copy_number_meta

files;

case_lists
X data_clinical_patient.txt
X data_clinical_sample.txt
data_CNA.ascna.txt
X (facets ; copy_number.cwl) data_CNA.txt
data_fusions.txt
(maf_filter.py) data_mutations_extended.txt
X meta_clinical_patient.txt
X meta_clinical_sample.txt
X meta_CNA.txt
X meta_fusions.txt
X meta_mutations_extended.txt
X meta_study.txt
pi_f8_3a_08390_G_data_cna_hg19.seg
pi_f8_3a_08390_G_meta_cna_hg19_seg.txt

https://github.com/cBioPortal/cbioportal/blob/master/docs/File-Formats.md#example-sample-data-file


need some portal_config_data from the inputs.yaml (get_meta_info), fields;
Assay
ProjectID (generateIGOBasedPortalUUID; stable_id)
ProjectTitle
ProjectDesc
PI
TumorType






Usage
-----

$ generate_cbioPortal_files.py patient --data-clinical-file ../test_data/inputs/Proj_08390_G_sample_data_clinical.txt

$ generate_cbioPortal_files.py sample --data-clinical-file ../test_data/inputs/Proj_08390_G_sample_data_clinical.txt --sample-summary-file ../test_data/qc/Proj_08390_G_SampleSummary.txt --project-pi orlowi --request-pi orlowi

$ generate_cbioPortal_files.py study --cancer-study-id cancer_study --name name --short-name short_name --type-of-cancer type_of_cancer --extra-groups foo_group --extra-groups bar_group

$ generate_cbioPortal_files.py meta_sample --cancer-study-id cancer_study

$ generate_cbioPortal_files.py meta_patient --cancer-study-id cancer_study

$ generate_cbioPortal_files.py meta_cna --cancer-study-id cancer_study

$ generate_cbioPortal_files.py meta_fusion --cancer-study-id cancer_study

$ generate_cbioPortal_files.py meta_mutations --cancer-study-id cancer_study
"""
import csv
import argparse
from collections import OrderedDict

# for each of the given header columns in the original data clinical file,
# need to add the following lines to the file
# preceeding the header line
header_lines_map = {
    'SAMPLE_ID' : {
    '1': 'SAMPLE_ID',
    '2': 'SAMPLE_ID',
    '3': 'STRING',
    '4': '1'
    },
    'IGO_ID' : {
    '1': 'IGO_ID',
    '2': 'IGO_ID',
    '3': 'STRING',
    '4': '1'
    },
    'PATIENT_ID': {
    '1': 'PATIENT_ID',
    '2': 'PATIENT_ID',
    '3': 'STRING',
    '4': '1'
    },
    'COLLAB_ID': {
    '1': 'COLLAB_ID',
    '2': 'COLLAB_ID',
    '3': 'STRING',
    '4': '0'
    },
    'SAMPLE_TYPE': {
    '1': 'SAMPLE_TYPE',
    '2': 'SAMPLE_TYPE',
    '3': 'STRING',
    '4': '1'
    },
    'SAMPLE_CLASS': {
    '1': 'SAMPLE_CLASS',
    '2': 'SAMPLE_CLASS',
    '3': 'STRING',
    '4': '1'
    },
    'GENE_PANEL': {
    '1': 'GENE_PANEL',
    '2': 'GENE_PANEL',
    '3': 'STRING',
    '4': '1'
    },
    'ONCOTREE_CODE': {
    '1': 'ONCOTREE_CODE',
    '2': 'ONCOTREE_CODE',
    '3': 'STRING',
    '4': '1'
    },
    'SPECIMEN_PRESERVATION_TYPE': {
    '1': 'SPECIMEN_PRESERVATION_TYPE',
    '2': 'SPECIMEN_PRESERVATION_TYPE',
    '3': 'STRING',
    '4': '1'
    },
    'SEX': {
    '1': 'SEX',
    '2': 'SEX',
    '3': 'STRING',
    '4': '1'
    },
    'TISSUE_SITE': {
    '1': 'TISSUE_SITE',
    '2': 'TISSUE_SITE',
    '3': 'STRING',
    '4': '1'
    },
    'REQUEST_ID': {
    '1': 'REQUEST_ID',
    '2': 'REQUEST_ID',
    '3': 'STRING',
    '4': '1'
    },
    'PROJECT_ID': {
    '1': 'PROJECT_ID',
    '2': 'PROJECT_ID',
    '3': 'STRING',
    '4': '1'
    },
    'PIPELINE': {
    '1': 'PIPELINE',
    '2': 'PIPELINE',
    '3': 'STRING',
    '4': '1'
    },
    'PIPELINE_VERSION': {
    '1': 'PIPELINE_VERSION',
    '2': 'PIPELINE_VERSION',
    '3': 'STRING',
    '4': '1'
    },
    'SAMPLE_COVERAGE': {
    '1': 'SAMPLE_COVERAGE',
    '2': 'SAMPLE_COVERAGE',
    '3': 'NUMBER',
    '4': '1'
    },
    'PROJECT_PI': {
    '1': 'PROJECT_PI',
    '2': 'PROJECT_PI',
    '3': 'STRING',
    '4': '1'
    },
    'REQUEST_PI': {
    '1': 'REQUEST_PI',
    '2': 'REQUEST_PI',
    '3': 'STRING',
    '4': '1'
    }
}


# Utility functions
def load_clinical_data(filepath):
    """
    Load the data clinical file contents

    Parameters
    ----------
    filepath: str
        the path to the data clinical file

    Returns
    -------
    list
        a list of OrderedDict's containing the values from the file
    """
    with open(filepath) as fin:
        reader = csv.DictReader(fin, delimiter = "\t")
        data = [ row for row in reader ]
    return(data)

def load_sample_coverages(filepath):
    """
    Load the sample summary file contents
    Need the samples and their coverages, only

    Parameters
    ----------
    filepath: str
        the path to the sample summary file containing 'Sample' and 'Coverage' columns

    Returns
    -------
    dict
        a dict of 'Sample':'Coverage' mappings
    """
    samples = {}
    with open(filepath) as fin:
        reader = csv.DictReader(fin, delimiter = "\t")
        for row in reader:
            samples[row['Sample']] = row['Coverage']
    # get rid of this extra row if present, its not a sample
    samples.pop('Project Average', None)
    return(samples)

def generate_portal_data_clinical_patient(clinical_data):
    """
    Generate the cBio Portal data for the data_clinical_patient.txt file
    based on data clinical entries from the original file

    data_clinical_patient.txt
    PATIENT_ID	SEX

    Parameters
    ----------
    clinical_data: list
        a list of dict's representing the clincal data loaded from file

    Returns
    -------
    list
        a list of dict's subset for just the keys used in the data_clinical_patient.txt file
    """
    clinical_patient_data = []
    for row in clinical_data:
        new_row = {}
        new_row['PATIENT_ID'] = row['PATIENT_ID']
        new_row['SEX'] = row['SEX']
        clinical_patient_data.append(new_row)
    return(clinical_patient_data)

def generate_portal_data_clinical_sample(clinical_data):
    """
    Generate the cBio Portal data for the data_clinical_sample.txt file
    based on the data clinical entries from the original file

    data_clinical_sample.txt
    SAMPLE_ID	PATIENT_ID	TISSUE_SITE	SAMPLE_COVERAGE	ONCOTREE_CODE	IGO_ID	PIPELINE	SAMPLE_TYPE	COLLAB_ID	GENE_PANEL	REQUEST_ID	SPECIMEN_PRESERVATION_TYPE	PIPELINE_VERSION	PROJECT_ID	SAMPLE_CLASS	PROJECT_PI	REQUEST_PI

    Parameters
    ----------
    clinical_data: list
        a list of dict's representing the clincal data loaded from file

    Returns
    -------
    list
        a list of dict's subset for just the keys used in the data_clinical_sample.txt file
    """
    cols_to_keep = [
    "SAMPLE_ID",
    "PATIENT_ID",
    "TISSUE_SITE",
    "SAMPLE_COVERAGE",
    "ONCOTREE_CODE",
    "IGO_ID",
    "PIPELINE",
    "SAMPLE_TYPE",
    "COLLAB_ID",
    "GENE_PANEL",
    "REQUEST_ID",
    "SPECIMEN_PRESERVATION_TYPE",
    "PIPELINE_VERSION",
    "PROJECT_ID",
    "SAMPLE_CLASS",
    "PROJECT_PI",
    "REQUEST_PI"
    ]
    clinical_sample_data = []
    for row in clinical_data:
        new_row = { key:value for key, value in row.items() if key in cols_to_keep }
        clinical_sample_data.append(new_row)
    return(clinical_sample_data)

def generate_header_lines(keys, delimiter = '\t', header_lines_map = header_lines_map):
    """
    Generate the extra header lines needed for the cBio Portal files
    https://github.com/cBioPortal/cbioportal/blob/master/docs/File-Formats.md#example-sample-data-file

    Parameters
    ----------
    keys: list
        a list of character string values for the columns, should correspond to values in `header_lines_map`
    delimiter: str
        the line delimiter value
    header_lines_map: dict
        the mapping of values for `1`, `2`, `3`, and `4` lines in the header for each key value

    Returns
    -------
    list
        a list of character strings representing the header lines to be printed to the file
    """
    lines_map = OrderedDict([
    ("1", "#"),
    ("2", "#"),
    ("3", "#"),
    ("4", "#")
    ])

    for key in keys:
        lines_map["1"] += header_lines_map[key]["1"] + delimiter
        lines_map["2"] += header_lines_map[key]["2"] + delimiter
        lines_map["3"] += header_lines_map[key]["3"] + delimiter
        lines_map["4"] += header_lines_map[key]["4"] + delimiter
    lines = []
    for line in lines_map.values():
        # remove trailing delimiters, add trailing newline
        lines.append(line.rstrip(delimiter) + '\n')
    return(lines)

def create_file_lines(clinical_data, delimiter = '\t'):
    """
    Create the lines in the file based on the provided clinical data
    First gets the header lines for the file, then generates each remaining line in the file

    Parameters
    ----------
    clinical_data: list
        a list of dict's containing the clinical data to be output as a new file

    Returns
    -------
    list
        a list of character strings representing each line to be written out to the file
    """
    lines = []

    # get the cBio header lines from the clinical data keys
    # assume the first entry has the same keys as the rest
    clinical_keys = [ k for k in clinical_data[0].keys() ]
    for header_line in generate_header_lines(clinical_keys, delimiter = delimiter):
        lines.append(header_line)

    # add the dict header line
    lines.append(delimiter.join(clinical_keys) + '\n')

    # concat the rest of the clinical data values based on the delimiter
    for row in clinical_data:
        line = delimiter.join(row.values())
        lines.append(line + '\n')
    return(lines)

def generate_extra_group_labels_string(extra_groups, exclude_groups = ('NA', 'PITT')):
    """
    """
    extra_groups_to_add = []
    for group in extra_groups:
        # groups must be uppercase and remove spaces (legacy requirement)
        group_upper = group.upper().replace(" ", "")
        if group_upper not in exclude_groups:
            extra_groups_to_add.append(group_upper)
    # concatenate all the group labels
    extra_groups_str = ';'.join(extra_groups_to_add)
    return(extra_groups_str)

def generate_meta_lines(data):
    """
    Convert a data dict into a list of string lines to write to be written to a file
    """
    lines = []
    for key, value in data.items():
        line_str = '{key}: {value}\n'.format(key = key, value = value)
        lines.append(line_str)
    return(lines)


# metadata generation functions
def generate_study_meta(
    cancer_study_identifier,
    description,
    name,
    short_name,
    type_of_cancer,
    groups = 'PRISM;COMPONC;VIALEA', # These groups can access everything
    extra_groups = None
    ):
    """
    Create a dict to hold study metadata to use with cBio Portal
    """
    if extra_groups != None:
        extra_groups_str = generate_extra_group_labels_string(extra_groups)
        groups = groups + ';' + extra_groups_str
    data = {
    'cancer_study_identifier' : cancer_study_identifier,
    'description': description.replace('\n', ''), # no newlines allowed (legacy requirement)
    'groups': groups,
    'name': name,
    'short_name': short_name,
    'type_of_cancer': type_of_cancer
    }
    return(data)

def generate_clinical_meta_samples_data(
    cancer_study_identifier,
    data_filename,
    datatype = 'SAMPLE_ATTRIBUTES',
    genetic_alteration_type = 'CLINICAL'
    ):
    """
    Create a dict to hold the samples metadata
    """
    data = {
    'cancer_study_identifier' : cancer_study_identifier,
    'datatype' : datatype,
    'genetic_alteration_type': genetic_alteration_type,
    'data_filename': data_filename
    }
    return(data)

def generate_clinical_meta_patient_data(
    cancer_study_identifier,
    data_filename,
    datatype = 'PATIENT_ATTRIBUTES',
    genetic_alteration_type = 'CLINICAL'
    ):
    """
    """
    data = {
    'cancer_study_identifier' : cancer_study_identifier,
    'datatype' : datatype,
    'genetic_alteration_type': genetic_alteration_type,
    'data_filename': data_filename
    }
    return(data)

def generate_clinical_meta_cna_data(
    cancer_study_identifier,
    data_filename,
    datatype = 'DISCRETE',
    genetic_alteration_type = 'COPY_NUMBER_ALTERATION',
    stable_id = 'cna', # legacy requirement
    show_profile_in_analysis_tab = "true",
    profile_name = 'Discrete Copy Number Data',
    profile_description = 'Discrete Copy Number Data'
    ):
    """
    """
    data = {
    'cancer_study_identifier' : cancer_study_identifier,
    'datatype' : datatype,
    'genetic_alteration_type': genetic_alteration_type,
    'data_filename': data_filename,
    'stable_id': stable_id,
    'show_profile_in_analysis_tab': show_profile_in_analysis_tab,
    'profile_name': profile_name,
    'profile_description': profile_description
    }
    return(data)

def generate_fusion_meta_data(
    cancer_study_identifier,
    data_filename,
    datatype = 'FUSION',
    genetic_alteration_type = 'FUSION',
    stable_id = 'fusion',
    show_profile_in_analysis_tab = "true",
    profile_description = 'Fusion data',
    profile_name = 'Fusions'
    ):
    """
    """
    data = {
    'cancer_study_identifier': cancer_study_identifier,
    'data_filename': data_filename,
    'datatype': datatype,
    'genetic_alteration_type': genetic_alteration_type,
    'stable_id': stable_id,
    'show_profile_in_analysis_tab': show_profile_in_analysis_tab,
    'profile_description': profile_description,
    'profile_name' : profile_name,
    }
    return(data)

def generate_mutation_meta_data(
    cancer_study_identifier,
    data_filename,
    genetic_alteration_type = 'MUTATION_EXTENDED',
    datatype = 'MAF',
    stable_id = 'mutations',
    show_profile_in_analysis_tab = "true",
    profile_description = 'Mutation data',
    profile_name = 'Mutations'
    ):
    """
    """
    data = {
    'cancer_study_identifier': cancer_study_identifier,
    'data_filename': data_filename,
    'genetic_alteration_type': genetic_alteration_type,
    'datatype': datatype,
    'stable_id': stable_id,
    'show_profile_in_analysis_tab': show_profile_in_analysis_tab,
    'profile_description': profile_description,
    'profile_name': profile_name
    }
    return(data)




# File generation functions
def generate_mutation_meta_data_file(**kwargs):
    """
    """
    output = kwargs.pop('output', 'meta_mutations_extended.txt')
    cancer_study_identifier = kwargs.pop('cancer_study_identifier')
    data_filename = kwargs.pop('data_filename', 'data_mutations_extended.txt')

    meta_data = generate_mutation_meta_data(
        cancer_study_identifier = cancer_study_identifier,
        data_filename = data_filename
        )

    lines = generate_meta_lines(meta_data)

    with open(output, "w") as fout:
        fout.writelines(lines)

def generate_fusion_meta_data_file(**kwargs):
    """
    """
    output = kwargs.pop('output', 'meta_fusions.txt')
    cancer_study_identifier = kwargs.pop('cancer_study_identifier')
    data_filename = kwargs.pop('data_filename', 'data_fusions.txt')

    meta_data = generate_fusion_meta_data(
        cancer_study_identifier = cancer_study_identifier,
        data_filename = data_filename
        )
    lines = generate_meta_lines(meta_data)

    with open(output, "w") as fout:
        fout.writelines(lines)

def generate_clinical_meta_cna_data_file(**kwargs):
    """
    """
    output = kwargs.pop('output', 'meta_CNA.txt')
    cancer_study_identifier = kwargs.pop('cancer_study_identifier')
    data_filename = kwargs.pop('data_filename', 'data_CNA.txt')

    meta_data = generate_clinical_meta_cna_data(
        cancer_study_identifier = cancer_study_identifier,
        data_filename = data_filename
    )
    lines = generate_meta_lines(meta_data)

    with open(output, "w") as fout:
        fout.writelines(lines)

def generate_clinical_meta_patient_data_file(**kwargs):
    """
    Generate the cBioPortal meta_clinical_patient file
    """
    output = kwargs.pop('output', 'meta_clinical_patient.txt')
    cancer_study_identifier = kwargs.pop('cancer_study_identifier')
    data_filename = kwargs.pop('data_filename', 'data_clinical_patient.txt')

    meta_data = generate_clinical_meta_patient_data(
        cancer_study_identifier = cancer_study_identifier,
        data_filename = data_filename
    )
    lines = generate_meta_lines(meta_data)

    with open(output, "w") as fout:
        fout.writelines(lines)

def generate_clinical_meta_samples_data_file(**kwargs):
    """
    Generate the cBioPortal meta_clinical_sample file
    """
    output = kwargs.pop('output', 'meta_clinical_sample.txt')
    cancer_study_identifier = kwargs.pop('cancer_study_identifier')
    data_filename = kwargs.pop('data_filename', 'data_clinical_sample.txt')

    meta_data = generate_clinical_meta_samples_data(
        cancer_study_identifier = cancer_study_identifier,
        data_filename = data_filename
    )
    lines = generate_meta_lines(meta_data)

    with open(output, "w") as fout:
        fout.writelines(lines)

def generate_study_meta_file(**kwargs):
    """
    Generate the cBioPortal study metadata file
    """
    output = kwargs.pop('output', 'data_clinical_sample.txt')
    cancer_study_identifier = kwargs.pop('cancer_study_identifier')
    name = kwargs.pop('name')
    short_name = kwargs.pop('short_name')
    type_of_cancer = kwargs.pop('type_of_cancer')
    description = kwargs.pop('description', '')
    extra_groups = [ group for group in kwargs.pop('extra_groups', []) ]

    args = {
    'cancer_study_identifier' : cancer_study_identifier,
    'description' : description,
    'name' : name,
    'short_name' : short_name,
    'type_of_cancer' : type_of_cancer
    }

    if len(extra_groups) > 0:
        args['extra_groups'] = extra_groups

    meta_data = generate_study_meta(**args)

    lines = generate_meta_lines(meta_data)

    with open(output, "w") as fout:
        fout.writelines(lines)

def generate_data_clinical_sample_file(**kwargs):
    """
    Generate the cBioPortal sample clinical data file
    """
    data_clinical_file = kwargs.pop('data_clinical_file')
    sample_summary_file = kwargs.pop('sample_summary_file', None)
    output = kwargs.pop('output', 'data_clinical_sample.txt')
    project_pi = kwargs.pop('project_pi', None)
    request_pi = kwargs.pop('request_pi', None)

    # load data from the files
    clinical_data = load_clinical_data(data_clinical_file)

    # add the matching coverages to the clincal data, or a '' empty value
    if sample_summary_file != None:
        sample_coverages = load_sample_coverages(sample_summary_file)
        for row in clinical_data:
            row['SAMPLE_COVERAGE'] = sample_coverages.get(row['SAMPLE_ID'], '')

    # add more optional values, if they were passed
    for row in clinical_data:
        if project_pi != None:
            row['PROJECT_PI'] = project_pi
        if request_pi != None:
            row['REQUEST_PI'] = request_pi

    # parse the data down to the values needed for the sample file
    clinical_sample_data = generate_portal_data_clinical_sample(clinical_data)

    # create the lines to output to the file
    lines = create_file_lines(clinical_sample_data)

    # write all the lines to file
    with open(output, "w") as fout:
        fout.writelines(lines)


def generate_data_clinical_patient_file(**kwargs):
    """
    Generate the cBioPortal patient clinical data file
    """
    data_clinical_file = kwargs.pop('data_clinical_file')
    output = kwargs.pop('output', 'data_clinical_patient.txt')

    # load data from the files
    clinical_data = load_clinical_data(data_clinical_file)

    # parse the data down to the values needed for the patient file
    clinical_patient_data = generate_portal_data_clinical_patient(clinical_data)

    # create the lines to output to the file
    lines = create_file_lines(clinical_patient_data)

    # write all the lines to file
    with open(output, "w") as fout:
        fout.writelines(lines)




def main():
    """
    Main control function when called as a script
    """
    # top level CLI arg parser; args common to all output files go here
    parser = argparse.ArgumentParser(description = 'Generate cBio Portal metadata files from various input files')
    # parser.add_argument('--data-clinical-file', dest = 'data_clinical_file', required = True, help = 'The data clinical source file')

    # add sub-parsers for specific file outputs
    subparsers = parser.add_subparsers(help ='Sub-commands available')

    # subparser for data_clinical_patient.txt
    patient = subparsers.add_parser('patient', help = 'Create the clinical patient data file')
    patient.add_argument('--output', dest = 'output', default = "data_clinical_patient.txt", help = 'The name of the output file')
    patient.add_argument('--data-clinical-file', dest = 'data_clinical_file', required = True, help = 'The data clinical source file')
    patient.set_defaults(func = generate_data_clinical_patient_file)

    # subparser for data_clinical_sample.txt
    sample = subparsers.add_parser('sample', help = 'Create the clinical sample data file')
    sample.add_argument('--output', dest = 'output', default = "data_clinical_sample.txt", help = 'Name of the output file')
    sample.add_argument('--data-clinical-file', dest = 'data_clinical_file', required = True, help = 'The data clinical source file')
    sample.add_argument('--sample-summary-file', dest = 'sample_summary_file', default = None, help = 'A supplemental sample summary file with coverage values to add to the output table')
    sample.add_argument('--project-pi', dest = 'project_pi', default = None, help = 'A Project PI value to add to entries in the table')
    sample.add_argument('--request-pi', dest = 'request_pi', default = None, help = 'A Request PI value to add to entries in the table')
    sample.set_defaults(func = generate_data_clinical_sample_file)

    # subparser for meta_study.txt
    study = subparsers.add_parser('study', help = 'Create the study metadata file')
    study.add_argument('--output', dest = 'output', default = "meta_study.txt", help = 'Name of the output file')
    study.add_argument('--cancer-study-id', dest = 'cancer_study_identifier', required = True, help = 'ID for the cancer study')
    study.add_argument('--description', dest = 'description', default = '', help = 'A description of the cancer study')
    study.add_argument('--name', dest = 'name', required = True, help = 'The name of the cancer study')
    study.add_argument('--short-name', dest = 'short_name', required = True, help = 'A short name used for display used on various web pages within the cBioPortal')
    study.add_argument('--type-of-cancer', dest = 'type_of_cancer', required = True, help = 'The cancer type abbreviation')
    study.add_argument('--extra-groups', dest = "extra_groups", default = [], action='append', help='Extra grouping labels (one per flag invocation, can be used multiple times)')
    study.set_defaults(func = generate_study_meta_file)

    # subparser for meta_clinical_sample.txt
    meta_sample = subparsers.add_parser('meta_sample', help = 'Create the sample metadata file')
    meta_sample.add_argument('--output', dest = 'output', default = "meta_clinical_sample.txt", help = 'Name of the output file')
    meta_sample.add_argument('--cancer-study-id', dest = 'cancer_study_identifier', required = True, help = 'ID for the cancer study')
    meta_sample.add_argument('--sample-data-filename', dest = 'data_filename', default = 'data_clinical_sample.txt', help = 'Filename of the associated data_clinical_sample file')
    meta_sample.set_defaults(func = generate_clinical_meta_samples_data_file)

    # subparser for meta_clinical_patient.txt
    meta_patient = subparsers.add_parser('meta_patient', help = 'Create the patient metadata file')
    meta_patient.add_argument('--output', dest = 'output', default = "meta_clinical_patient.txt", help = 'Name of the output file')
    meta_patient.add_argument('--cancer-study-id', dest = 'cancer_study_identifier', required = True, help = 'ID for the cancer study')
    meta_patient.add_argument('--patient-data-filename', dest = 'data_filename', default = 'data_clinical_patient.txt', help = 'Filename of the associated data_clinical_patient file')
    meta_patient.set_defaults(func = generate_clinical_meta_patient_data_file)

    # subparser for meta_CNA.txt
    meta_cna = subparsers.add_parser('meta_cna', help = 'Create the Copy Number Alteration metadata file')
    meta_cna.add_argument('--output', dest = 'output', default = "meta_CNA.txt", help = 'Name of the output file')
    meta_cna.add_argument('--cancer-study-id', dest = 'cancer_study_identifier', required = True, help = 'ID for the cancer study')
    meta_cna.add_argument('--cna-data-filename', dest = 'data_filename', default = 'data_CNA.txt', help = 'Filename of the associated Copy Number Alteration data file')
    meta_cna.set_defaults(func = generate_clinical_meta_cna_data_file)

    # subparser for meta_fusions.txt
    meta_fusion = subparsers.add_parser('meta_fusion', help = 'Create the Fusion metadata file')
    meta_fusion.add_argument('--output', dest = 'output', default = "meta_fusions.txt", help = 'Name of the output file')
    meta_fusion.add_argument('--cancer-study-id', dest = 'cancer_study_identifier', required = True, help = 'ID for the cancer study')
    meta_fusion.add_argument('--fusion-data-filename', dest = 'data_filename', default = 'data_fusions.txt', help = 'Filename of the associated fusion data file')
    meta_fusion.set_defaults(func = generate_fusion_meta_data_file)

    # subparser for meta_mutations_extended.txt
    meta_mutations = subparsers.add_parser('meta_mutations', help = 'Create the Mutations metadata file')
    meta_mutations.add_argument('--output', dest = 'output', default = "meta_mutations_extended.txt", help = 'Name of the output file')
    meta_mutations.add_argument('--cancer-study-id', dest = 'cancer_study_identifier', required = True, help = 'ID for the cancer study')
    meta_mutations.add_argument('--mutations-data-filename', dest = 'data_filename', default = 'data_mutations_extended.txt', help = 'Filename of the mutations file')
    meta_mutations.set_defaults(func = generate_mutation_meta_data_file)




    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    main()
