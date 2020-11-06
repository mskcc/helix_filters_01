#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module + script to create files for cBioPortal for a cancer analysis

( ported over from roslin_analysis_helper.py )

Files that need to be created for cBioPortal:

portal/
├── case_lists
│   ├── cases_all.txt (X)
│   ├── cases_cnaseq.txt (X)
│   ├── cases_cna.txt (X)
│   └── cases_sequenced.txt (X)
├── data_clinical_patient.txt (X)
├── data_clinical_sample.txt (X)
├── data_CNA.ascna.txt (X from facets genelevel workflow along with data_CNA.scna.txt)
├── data_CNA.txt (X  from facets workflow ; copy_number.cwl)
├── data_fusions.txt (X in workflow.makefile, needs CWL )
├── data_mutations_extended.txt (X from maf_filter.py; TODO: split this into a separate script)
├── meta_clinical_patient.txt (X)
├── meta_clinical_sample.txt (X)
├── meta_CNA.txt (X)
├── meta_fusions.txt (X)
├── meta_mutations_extended.txt (X)
├── meta_study.txt (X)
├── <project_id>_data_cna_hg19.seg (X from reduce_sig_figs.cwl + concat.cwl)
└── <project_id>_meta_cna_hg19_seg.txt (X)


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

# data_clinical_patient.txt
$ generate_cbioPortal_files.py patient --data-clinical-file ../test_data/inputs/Proj_08390_G_sample_data_clinical.txt

# data_clinical_sample.txt
$ generate_cbioPortal_files.py sample --data-clinical-file ../test_data/inputs/Proj_08390_G_sample_data_clinical.txt --sample-summary-file ../test_data/qc/Proj_08390_G_SampleSummary.txt --project-pi pi_name --request-pi pi_name

# meta_study.txt
$ generate_cbioPortal_files.py study --cancer-study-id cancer_study_1 --name name --short-name short_name --type-of-cancer type_of_cancer --extra-groups foo_group --extra-groups bar_group

# meta_clinical_sample.txt
$ generate_cbioPortal_files.py meta_sample --cancer-study-id cancer_study_1

# meta_clinical_patient.txt
$ generate_cbioPortal_files.py meta_patient --cancer-study-id cancer_study_1

# meta_CNA.txt
$ generate_cbioPortal_files.py meta_cna --cancer-study-id cancer_study_1

# meta_fusions.txt
$ generate_cbioPortal_files.py meta_fusion --cancer-study-id cancer_study_1

# meta_mutations_extended.txt
$ generate_cbioPortal_files.py meta_mutations --cancer-study-id cancer_study_1

# <project_id>_meta_cna_hg19_seg.txt
$ generate_cbioPortal_files.py meta_segments --cancer-study-id cancer_study_1 --output cancer_study_1_meta_cna_hg19_seg.txt --segmented-data-file cancer_study_1_data_cna_hg19.seg

# cases_all.txt
$ generate_cbioPortal_files.py cases_all  --cancer-study-id cancer_study_1 --data-clinical-file ../test_data/inputs/Proj_08390_G_sample_data_clinical.txt

# cases_cnaseq.txt
$ generate_cbioPortal_files.py cases_cnaseq --cancer-study-id cancer_study --data-clinical-file ../test_data/inputs/Proj_08390_G_sample_data_clinical.txt

# cases_cna.txt
$ generate_cbioPortal_files.py cases_cna --cancer-study-id cancer_study --data-clinical-file ../test_data/inputs/Proj_08390_G_sample_data_clinical.txt

# cases_sequenced.txt
$ generate_cbioPortal_files.py cases_sequenced --cancer-study-id cancer_study --data-clinical-file ../test_data/inputs/Proj_08390_G_sample_data_clinical.txt
"""
import csv
import argparse
# from collections import OrderedDict

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .cBioPortal_utils import header_lines_map
    from .cBioPortal_utils import generate_header_lines
    from .cBioPortal_utils import create_file_lines
    from .cBioPortal_utils import parse_facets_data
    from .cBioPortal_utils import update_sample_data
    from .cBioPortal_utils import load_facets_data

if __name__ == "__main__":
    from cBioPortal_utils import header_lines_map
    from cBioPortal_utils import generate_header_lines
    from cBioPortal_utils import create_file_lines
    from cBioPortal_utils import parse_facets_data
    from cBioPortal_utils import update_sample_data
    from cBioPortal_utils import load_facets_data


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
    patient_ids = {} # use this dict to prevent duplicate patient IDs from being emitted
    clinical_patient_data = []
    for row in clinical_data:
        if row['PATIENT_ID'] not in patient_ids:
            new_row = {}
            new_row['PATIENT_ID'] = row['PATIENT_ID']
            new_row['SEX'] = row['SEX']
            clinical_patient_data.append(new_row)
            patient_ids[row['PATIENT_ID']] = ''
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

def get_sample_list(data):
    """
    Get a list of all the sample ID's in the data set

    Parameters
    ----------
    data: list
        a list of dict's with the key `SAMPLE_ID`

    Returns
    -------
    list
        a list of strings representing the sample IDs
    """
    sample_list = []
    for item in data:
        sample_list.append(item['SAMPLE_ID'])
    return(sample_list)


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

def generate_clinical_meta_samples_data(cancer_study_identifier, data_filename):
    """
    Create a dict to hold the samples metadata
    """
    data = {
    'cancer_study_identifier' : cancer_study_identifier,
    'datatype' : 'SAMPLE_ATTRIBUTES',
    'genetic_alteration_type': 'CLINICAL',
    'data_filename': data_filename
    }
    return(data)

def generate_clinical_meta_patient_data(cancer_study_identifier, data_filename):
    """
    """
    data = {
    'cancer_study_identifier' : cancer_study_identifier,
    'datatype' : 'PATIENT_ATTRIBUTES',
    'genetic_alteration_type': 'CLINICAL',
    'data_filename': data_filename
    }
    return(data)

def generate_clinical_meta_cna_data(cancer_study_identifier, data_filename):
    """
    """
    data = {
    'cancer_study_identifier' : cancer_study_identifier,
    'datatype' : 'DISCRETE',
    'genetic_alteration_type': 'COPY_NUMBER_ALTERATION',
    'data_filename': data_filename,
    'stable_id': 'cna',
    'show_profile_in_analysis_tab': "true",
    'profile_name': 'Discrete Copy Number Data',
    'profile_description': 'Discrete Copy Number Data'
    }
    return(data)

def generate_fusion_meta_data(cancer_study_identifier, data_filename):
    """
    """
    data = {
    'cancer_study_identifier': cancer_study_identifier,
    'data_filename': data_filename,
    'datatype': 'FUSION',
    'genetic_alteration_type': 'FUSION',
    'stable_id': 'fusion',
    'show_profile_in_analysis_tab': "true",
    'profile_description': 'Fusion data',
    'profile_name' : 'Fusions',
    }
    return(data)

def generate_mutation_meta_data(cancer_study_identifier, data_filename):
    """
    """
    data = {
    'cancer_study_identifier': cancer_study_identifier,
    'data_filename': data_filename,
    'genetic_alteration_type': 'MUTATION_EXTENDED',
    'datatype': 'MAF',
    'stable_id': 'mutations',
    'show_profile_in_analysis_tab': "true",
    'profile_description': 'Mutation data',
    'profile_name': 'Mutations'
    }
    return(data)

def generate_case_list_all_data(cancer_study_identifier, case_list_ids):
    """
    case_list_ids: list
        a list of strings representing the case list id's
    """
    data = {
    'cancer_study_identifier': cancer_study_identifier,
    'stable_id': cancer_study_identifier + '_all',
    'case_list_category': 'all_cases_in_study',
    'case_list_name': 'All Tumors',
    'case_list_description': 'All tumor samples',
    'case_list_ids': '\t'.join(case_list_ids)
    }
    return(data)

def generate_case_list_cnaseq_data(cancer_study_identifier, case_list_ids):
    """
    """
    data = {
    'cancer_study_identifier': cancer_study_identifier,
    'stable_id': cancer_study_identifier + '_cnaseq',
    'case_list_ids': '\t'.join(case_list_ids),
    'case_list_category': 'all_cases_with_mutation_and_cna_data',
    'case_list_name': 'Tumors with sequencing and CNA data',
    'case_list_description': 'All tumor samples that have CNA and sequencing data'
    }
    return(data)

def generate_case_list_cna_data(cancer_study_identifier, case_list_ids):
    """
    """
    data = {
    'cancer_study_identifier': cancer_study_identifier,
    'stable_id': cancer_study_identifier + '_cna',
    'case_list_ids': '\t'.join(case_list_ids),
    'case_list_category': "all_cases_with_cna_data",
    'case_list_name': "Tumors CNA",
    'case_list_description': "All tumors with CNA data"
    }
    return(data)

def generate_case_list_sequenced_data(cancer_study_identifier, case_list_ids):
    """
    """
    data = {
    'cancer_study_identifier': cancer_study_identifier,
    'stable_id': cancer_study_identifier + '_sequenced',
    'case_list_ids': '\t'.join(case_list_ids),
    'case_list_category': "all_cases_with_mutation_data",
    'case_list_name': "Sequenced Tumors",
    'case_list_description': "All sequenced tumors"
    }
    return(data)

def generate_meta_segments_data(cancer_study_identifier, data_filename):
    """
    """
    data = {
    'cancer_study_identifier': cancer_study_identifier,
    'data_filename': data_filename,
    'genetic_alteration_type': 'COPY_NUMBER_ALTERATION',
    'datatype': 'SEG',
    'description': 'Segmented Data',
    'reference_genome_id': 'hg19'
    }
    return(data)

def clean_facets_suite_cna_header(col_labels):
    """
    Some files output by Facets Suite have '_hisens' appended to the sample IDs, need to test that this gets detected and removed

    affected files;

    portal/data_CNA.txt
    portal/data_CNA.ascna.txt
    """
    new_labels = []
    for label in col_labels:
        if label.endswith('_hisens'):
            new_label = label.rstrip('_hisens')
            new_labels.append(new_label)
        else:
            new_labels.append(label)
    return(new_labels)



#
#
# File generation functions
#
#
def generate_meta_segments_data_file(**kwargs):
    """
    """
    output = kwargs.pop('output')
    cancer_study_identifier = kwargs.pop('cancer_study_identifier')
    data_filename = kwargs.pop('data_filename')

    meta_data = generate_meta_segments_data(cancer_study_identifier = cancer_study_identifier, data_filename = data_filename)

    lines = generate_meta_lines(meta_data)

    with open(output, "w") as fout:
        fout.writelines(lines)

def generate_cases_sequenced_data_file(**kwargs):
    """
    data_clinical_file only needed to get sample ID's
    """
    output = kwargs.pop('output', 'cases_sequenced.txt')
    cancer_study_identifier = kwargs.pop('cancer_study_identifier')
    data_clinical_file = kwargs.pop('data_clinical_file')

    clinical_data = load_clinical_data(data_clinical_file)

    sample_list = get_sample_list(clinical_data)

    cases_data = generate_case_list_sequenced_data(cancer_study_identifier = cancer_study_identifier, case_list_ids = sample_list)

    lines = generate_meta_lines(cases_data)

    with open(output, "w") as fout:
        fout.writelines(lines)

def generate_cases_cna_data_file(**kwargs):
    """
    data_clinical_file only needed to get sample ID's
    """
    output = kwargs.pop('output', 'cases_cna.txt')
    cancer_study_identifier = kwargs.pop('cancer_study_identifier')
    data_clinical_file = kwargs.pop('data_clinical_file')

    clinical_data = load_clinical_data(data_clinical_file)

    sample_list = get_sample_list(clinical_data)

    cases_data = generate_case_list_cna_data(cancer_study_identifier = cancer_study_identifier, case_list_ids = sample_list)

    lines = generate_meta_lines(cases_data)

    with open(output, "w") as fout:
        fout.writelines(lines)

def generate_cases_cnaseq_data_file(**kwargs):
    """
    data_clinical_file only needed to get sample ID's
    """
    output = kwargs.pop('output', 'cases_cnaseq.txt')
    cancer_study_identifier = kwargs.pop('cancer_study_identifier')
    data_clinical_file = kwargs.pop('data_clinical_file')

    clinical_data = load_clinical_data(data_clinical_file)

    sample_list = get_sample_list(clinical_data)

    cases_data = generate_case_list_cnaseq_data(cancer_study_identifier = cancer_study_identifier, case_list_ids = sample_list)

    lines = generate_meta_lines(cases_data)

    with open(output, "w") as fout:
        fout.writelines(lines)

def generate_case_list_all_data_file(**kwargs):
    """
    data_clinical_file only needed to get sample ID's
    """
    output = kwargs.pop('output', 'cases_all.txt')
    cancer_study_identifier = kwargs.pop('cancer_study_identifier')
    data_clinical_file = kwargs.pop('data_clinical_file')

    clinical_data = load_clinical_data(data_clinical_file)

    sample_list = get_sample_list(clinical_data)

    cases_data = generate_case_list_all_data(cancer_study_identifier = cancer_study_identifier, case_list_ids = sample_list)

    lines = generate_meta_lines(cases_data)

    with open(output, "w") as fout:
        fout.writelines(lines)


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
    facets_txt_files = kwargs.pop('facets_txt_files', [])
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

    # if facets data is provided, load it
    all_facets_data = []
    parsed_facets_data = None
    if facets_txt_files:
        parsed_facets_data = load_facets_data(facets_txt_files)

    # add more optional values, if they were passed
    for row in clinical_data:
        if project_pi != None:
            row['PROJECT_PI'] = project_pi
        if request_pi != None:
            row['REQUEST_PI'] = request_pi

    # parse the data down to the values needed for the sample file
    clinical_sample_data = generate_portal_data_clinical_sample(clinical_data)

    updated_sample_data = []
    if parsed_facets_data != None:
        # update all the sample datas based on facets data
        for sample_data in clinical_sample_data:
            new_sample_data = update_sample_data(sample_data, facets_data = parsed_facets_data)
            updated_sample_data.append(new_sample_data)

    # create the lines to output to the file
    if updated_sample_data:
        lines = create_file_lines(updated_sample_data)
    else:
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

def clean_facets_suite_cna_file(**kwargs):
    """
    Some files output by Facets Suite have '_hisens' appended to the sample IDs, need to test that this gets detected and removed

    affected files;

    portal/data_CNA.txt
    portal/data_CNA.ascna.txt
    """
    input_file = kwargs.pop('input_file')
    output_file = kwargs.pop('output_file')
    with open(input_file) as fin, open(output_file, "w") as fout:
        header_labels = next(fin).split() # tab delimited
        clean_header_labels = clean_facets_suite_cna_header(header_labels)
        clean_header_line = '\t'.join(clean_header_labels) + '\n'
        fout.write(clean_header_line)
        for line in fin:
            fout.write(line)

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
    sample.add_argument('--facets-txt-files', dest = 'facets_txt_files', nargs='*', help = 'The .txt output files from Facets Suite')
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

    # subparser for cases_all.txt
    cases_all = subparsers.add_parser('cases_all', help = 'Create the file for the all case list file')
    cases_all.add_argument('--output', dest = 'output', default = "cases_all.txt", help = 'Name of the output file')
    cases_all.add_argument('--cancer-study-id', dest = 'cancer_study_identifier', required = True, help = 'ID for the cancer study')
    cases_all.add_argument('--data-clinical-file', dest = 'data_clinical_file', required = True, help = 'The data clinical source file')
    cases_all.set_defaults(func = generate_case_list_all_data_file)

    # subparser for cases_cnaseq.txt
    cases_cnaseq = subparsers.add_parser('cases_cnaseq', help = 'Create the file for the samples with copy number and sequencing case list file')
    cases_cnaseq.add_argument('--output', dest = 'output', default = "cases_cnaseq.txt", help = 'Name of the output file')
    cases_cnaseq.add_argument('--cancer-study-id', dest = 'cancer_study_identifier', required = True, help = 'ID for the cancer study')
    cases_cnaseq.add_argument('--data-clinical-file', dest = 'data_clinical_file', required = True, help = 'The data clinical source file')
    cases_cnaseq.set_defaults(func = generate_cases_cnaseq_data_file)

    # subparser for cases_cna.txt
    cases_cna = subparsers.add_parser('cases_cna', help = 'Create the file for the samples with copy number case list file')
    cases_cna.add_argument('--output', dest = 'output', default = "cases_cna.txt", help = 'Name of the output file')
    cases_cna.add_argument('--cancer-study-id', dest = 'cancer_study_identifier', required = True, help = 'ID for the cancer study')
    cases_cna.add_argument('--data-clinical-file', dest = 'data_clinical_file', required = True, help = 'The data clinical source file')
    cases_cna.set_defaults(func = generate_cases_cna_data_file)

    # cases_sequenced.txt
    cases_sequenced = subparsers.add_parser('cases_sequenced', help = 'Create the file for the samples with copy number case list file')
    cases_sequenced.add_argument('--output', dest = 'output', default = "cases_sequenced.txt", help = 'Name of the output file')
    cases_sequenced.add_argument('--cancer-study-id', dest = 'cancer_study_identifier', required = True, help = 'ID for the cancer study')
    cases_sequenced.add_argument('--data-clinical-file', dest = 'data_clinical_file', required = True, help = 'The data clinical source file')
    cases_sequenced.set_defaults(func = generate_cases_sequenced_data_file)

    # subparser _meta_cna_hg19_seg.txt for _data_cna_hg19.seg file
    meta_segments = subparsers.add_parser('meta_segments', help = 'Create the Segmented data metadata file')
    meta_segments.add_argument('--output', dest = 'output', required = True, default = "_meta_cna_hg19_seg.txt", help = 'Name of the output file')
    meta_segments.add_argument('--cancer-study-id', dest = 'cancer_study_identifier', required = True, help = 'ID for the cancer study')
    meta_segments.add_argument('--segmented-data-file', dest = 'data_filename', required = True, default = '_data_cna_hg19.seg', help = 'Filename of the mutations file')
    meta_segments.set_defaults(func = generate_meta_segments_data_file)

    clean_cna = subparsers.add_parser('clean_cna', help = 'Clean the Facets Suite CNA file')
    clean_cna.add_argument('--output', dest = 'output_file', required = True, help = 'Name of the output file')
    clean_cna.add_argument('--input', dest = 'input_file', required = True, help = 'Name of the input file')
    clean_cna.set_defaults(func = clean_facets_suite_cna_file)


    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    main()
