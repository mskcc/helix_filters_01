#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for cBioPortal file and data handling
"""
from collections import OrderedDict

# keep only these columns, and rename them to the listed values
facets_data_keep_cols_map = { # old:new
    "purity": "ASCN_PURITY",
    "ploidy": "ASCN_PLOIDY",
    "facets_version": "ASCN_VERSION",
    "genome_doubled": "ASCN_WGD"
}

# remove these columns from data_clinical_sample.txt data while updating it with Facets Suite data
sample_data_remove_cols = ["purity", "ploidy", "facets_version"]

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
    },
    'ASCN_PURITY': {
    '1': 'ASCN_PURITY',
    '2': 'ASCN_PURITY',
    '3': 'NUMBER',
    '4': '1'
    },
    'ASCN_PLOIDY': {
    '1': 'ASCN_PLOIDY',
    '2': 'ASCN_PLOIDY',
    '3': 'NUMBER',
    '4': '1'
    },
    'ASCN_VERSION': {
    '1': 'ASCN_VERSION',
    '2': 'ASCN_VERSION',
    '3': 'STRING',
    '4': '0'
    },
    'genome_doubled': {
    '1': 'genome_doubled',
    '2': 'genome_doubled',
    '3': 'STRING',
    '4': '0'
    },
    'ASCN_WGD': {
    '1': 'ASCN_WGD',
    '2': 'ASCN_WGD',
    '3': 'STRING',
    '4': '1'
    }
}

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


def update_sample_data(sample_data, facets_data):
    """
    Add entries to the sample data based on values from the facets data

    Parameters
    ----------
    sample_data: dict
        a dict representing a row of sample data from the data_clinical_sample.txt file
    facets_data: dict
        a dict of facets hisens entries per sample from the Facets Suite aggregate txt file

    Returns
    -------
    dict
        an updted copy of the `sample_data` dict with matching values from the `facets_data` dict
    """
    d = { k:v for k, v in sample_data.items() }
    sample_id = d['SAMPLE_ID']
    # add matching facets data
    if sample_id in facets_data:
        d = { **d, **facets_data[sample_id] }
    else:
        # add NA for the facets columns instead
        for k,v in facets_data_keep_cols_map.items():
            d[k] = "NA"
            d[v] = "NA"
    # get rid of undesired columns
    for key in sample_data_remove_cols:
        if key in d:
            d.pop(key)
    return(d)

def parse_facets_data(rows):
    """
    Need to dig through the data output by Facets Suite .txt files in order to return a dict of per sample info
    that has only the desired info from "hisens" rows
    """
    data = {}
    for row in rows:
        # only keep 'hisens' rows
        if row['run_type'] != "hisens":
            continue
        else:
            # keep only desired columns
            d = { key:row[key] for key in facets_data_keep_cols_map.keys() }
            # add the renamed columns
            for old_key, new_key in facets_data_keep_cols_map.items():
                d[new_key] = d[old_key]
            # change the "genome_doubled" value
            if d["genome_doubled"] == "TRUE":
                d["ASCN_WGD"] = "WGD"
            elif d["genome_doubled"] == "FALSE":
                d["ASCN_WGD"] = "no WGD"

            # NOTE:
            # convention earlier in the pipeline was that Facets Suite "sample_id" = TumorID.NormalID
            # we need to use only the Tumor ID here because that is what matches up with the values in
            # data_clinical_sample.txt
            # so, split on '.' here an keep the first item and assume its the Tumor ID
            # TODO: get Facets Suite run-facets-wrapper.R script to embed the tumor and normal ID values into the file
            # so we dont have to do this
            # NOTE: follow up; added steps to CWL workflow to add our own 'sample' and 'tumor' labels to file so we should deprecate this
            sample_id = row['sample'].split('.')[0]
            data[sample_id] = d
    return(data)