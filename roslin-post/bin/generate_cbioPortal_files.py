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

https://github.com/cBioPortal/cbioportal/blob/master/docs/File-Formats.md#example-sample-data-file
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
    # 'COLLAB_ID': { # this does not get included in output files
    # '1': 'COLLAB_ID',
    # '2': 'COLLAB_ID',
    # '3': 'STRING',
    # '4': '1'
    # }
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

}

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

def generate_data_clinical_patient(**kwargs):
    """
    """
    data_clinical_file = kwargs.pop('data_clinical_file')
    sample_summary_file = kwargs.pop('sample_summary_file')
    output = kwargs.pop('output', 'data_clinical_patient.txt')

    # load data from the files
    clinical_data = load_clinical_data(data_clinical_file)
    sample_coverages = load_sample_coverages(sample_summary_file)

    # parse the data down the values needed for the patient file
    clinical_patient_data = generate_portal_data_clinical_patient(clinical_data)

    # create the lines to output to the file
    lines = create_file_lines(clinical_patient_data)

    with open(output, "w") as fout:
        fout.writelines(lines)
    # for line in lines:
    #     print(line)

    # for row in clinical_data:
    #     # add the matching coverages to the clincal data, or a '' empty value
    #     row['SAMPLE_COVERAGE'] = sample_coverages.get(row['SAMPLE_ID'], '')
        # print(row)


def main():
    """
    Main control function when called as a script
    """
    parser = argparse.ArgumentParser(description = 'Generate cBio Portal metadata files from various input files')
    subparsers = parser.add_subparsers(help ='Sub-commands available')

    # subparser for data_clinical_patient.txt
    patient = subparsers.add_parser('patient', help = 'Create the clinical patient data file')
    patient.add_argument('--data-clinical-file', dest = 'data_clinical_file', required = True, help = 'The data clinical source file')
    patient.add_argument('--sample-summary-file', dest = 'sample_summary_file', required = True, help = 'The sample summary file with coverage values')
    patient.add_argument('--output', dest = 'output', default = "data_clinical_patient.txt", help = 'The sample summary file with coverage values')
    patient.set_defaults(func = generate_data_clinical_patient)

    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    main()
