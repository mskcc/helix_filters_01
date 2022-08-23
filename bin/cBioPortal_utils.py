#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for cBioPortal file and data handling

-----
NOTE: MOVE MAF OUTPUT AND FORMATTER TO cBioPortal_utils.MafWriter !! DO NOT ADD MORE ONE-OFF MAF FORMATTING MODULES AND METHODS !!
-----
NOTE: see also
pluto.tools.TableReader
pluto.tools.MafWriter
https://github.com/mskcc/pluto/blob/e10fd75b9f384b8d13ff84f6c955e08b2c354b4f/tools.py#L687
-----
"""
import csv
from collections import OrderedDict
from typing import TextIO, List, Dict, Tuple


#
# CONSTANTS & GLOBALS
#

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
    'SAMPLE_ID' : { # original column header label
    '1': 'SAMPLE_ID', # pretty-printed column header label; shown as cBioPortal webpage table header
    '2': 'SAMPLE_ID', # this should be the hover-text in cBioPortal table header (?)
    '3': 'STRING', # data type for the column in cBioPortal
    '4': '1' # show this column in cBioPortal or not (0 = hide, 1 = show)
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
    },
    # added these column headers for use with TMB reporting
    'CMO_TMB_SCORE': {
    '1': 'CMO_TMB_SCORE',
    '2': 'CMO_TMB_SCORE',
    '3': 'NUMBER',
    '4': '1'
    },

    # added these column headers for use with MSIsensor
    # 'Total_Number_of_Sites': {
    # '1': 'CMO_MSI_SCORE',
    # '2': 'CMO_MSI_SCORE',
    # '3': 'NUMBER',
    # '4': '0'
    # },
    # 'Number_of_Somatic_Sites': {
    # '1': 'CMO_MSI_SOMATIC_SITES',
    # '2': 'CMO_MSI_SOMATIC_SITES',
    # '3': 'NUMBER',
    # '4': '0'
    # },
    'MSI_SCORE': {
    '1': 'CMO_MSI_SCORE',
    '2': 'CMO_MSI_SCORE',
    '3': 'NUMBER',
    '4': '0'
    },
    'MSI_STATUS': {
    '1': 'CMO_MSI_STATUS',
    '2': 'CMO_MSI_STATUS',
    '3': 'STRING',
    '4': '0'
    }

}

maf_filter_portal_file_cols_to_keep = [
"Hugo_Symbol",
"Entrez_Gene_Id",
"Center",
"NCBI_Build",
"Chromosome",
"Start_Position",
"End_Position",
"Strand",
"Variant_Classification",
"Variant_Type",
"Reference_Allele",
"Tumor_Seq_Allele1",
"Tumor_Seq_Allele2",
"dbSNP_RS",
"dbSNP_Val_Status",
"Tumor_Sample_Barcode",
"Matched_Norm_Sample_Barcode",
"Match_Norm_Seq_Allele1",
"Match_Norm_Seq_Allele2",
"Tumor_Validation_Allele1",
"Tumor_Validation_Allele2",
"Match_Norm_Validation_Allele1",
"Match_Norm_Validation_Allele2",
"Verification_Status",
"Validation_Status",
"Mutation_Status",
"Sequencing_Phase",
"Sequence_Source",
"Validation_Method",
"Score",
"BAM_File",
"Sequencer",
"Tumor_Sample_UUID",
"Matched_Norm_Sample_UUID",
"HGVSc",
"HGVSp",
# "HGVSp_Short", # need to not output this in portal file !!
"Amino_Acid_Change",
"Transcript_ID",
"Exon_Number",
"t_depth",
"t_ref_count",
"t_alt_count",
"n_depth",
"n_ref_count",
"n_alt_count",
"ASCN.TOTAL_COPY_NUMBER",
"ASCN.MINOR_COPY_NUMBER",
"ASCN.EXPECTED_ALT_COPIES",
"ASCN.CCF_EXPECTED_COPIES",
"ASCN.CCF_EXPECTED_COPIES_LOWER",
"ASCN.CCF_EXPECTED_COPIES_UPPER",
"ASCN.ASCN_METHOD",
"ASCN.ASCN_INTEGER_COPY_NUMBER",
"ASCN.CLONAL" #  comes from the same facets file as ASCN.TOTAL_COPY_NUMBER https://github.com/mskcc/pluto-cwl/issues/22
]


#
# FUNCTIONS
#

def generate_header_lines(
        keys: List[str],
        delimiter: str = '\t',
        header_lines_map: Dict = header_lines_map) -> List[str]:
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
        try:
            lines_map["1"] += header_lines_map[key]["1"] + delimiter
            lines_map["2"] += header_lines_map[key]["2"] + delimiter
            lines_map["3"] += header_lines_map[key]["3"] + delimiter
            lines_map["4"] += header_lines_map[key]["4"] + delimiter
        except KeyError: # the column header key is not in the mapping; use a dummy value
            lines_map["1"] += key + delimiter
            lines_map["2"] += key + delimiter
            lines_map["3"] += key + delimiter
            lines_map["4"] += "0" + delimiter
    lines = []
    for line in lines_map.values():
        # remove trailing delimiters, add trailing newline
        lines.append(line.rstrip(delimiter) + '\n')
    return(lines)

def create_file_lines(
        clinical_data: List[Dict],
        delimiter: str = '\t',
        na_str: str = 'NA') -> List[str]:
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

    # get the cBio header lines from the clinical data keys;
    # need to get set of all keys in all records
    # clinical_keys = list(set().union(*(d.keys() for d in clinical_data))) # this way is better but loses ordering
    # use an OrderedDict to preserve ordering
    clinical_keys = OrderedDict()
    for d in clinical_data:
        for k in d.keys():
            clinical_keys[k] = None # I think None is the smallest byte size value, 16bytes each
    clinical_keys = clinical_keys.keys() # final list of keys in the desired order
    for header_line in generate_header_lines(clinical_keys, delimiter = delimiter):
        lines.append(header_line)

    # add the dict header line
    lines.append(delimiter.join(clinical_keys) + '\n')

    # concat the rest of the clinical data values based on the delimiter
    for row in clinical_data:
        # need to make sure that output values match the order of the header keys
        new_row = OrderedDict()
        for key in clinical_keys:
            value = row.get(key, na_str) # fill in missing values with na_str
            # need to check if a None value was originally passed in the clincial data;
            # this originates from blank empty cell in the data_clinical_sample.txt file
            if value is None:
                value = na_str
            new_row[key] = value
        # concat the values into a single string for printing
        line = delimiter.join(new_row.values())
        lines.append(line + '\n')
    return(lines)


def update_sample_data(sample_data: Dict, facets_data: Dict) -> Dict:
    """
    Add entries to the sample data based on values from the facets data

    NOTE: this functionality is partially deprecated by merge-tables.py script; see that script for future need to merge in new columns

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

def parse_facets_data(rows: List[Dict]) -> Dict:
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

def load_facets_data(files: List[str]) -> Dict:
    """
    Load the data from all Facets Suite .txt files in the files list
    """
    all_data = {}
    for file in files:
        all_facets_data = []
        with open(file) as fin:
            reader = csv.DictReader(fin, delimiter = '\t')
            for row in reader:
                all_facets_data.append(row)

        # clean up the facets data to remove stuff we dont want and recalculate things
        parsed_facets_data = parse_facets_data(all_facets_data)
        all_data = {**all_data, **parsed_facets_data}
    return(all_data)

def parse_header_comments(filename: str, comment_char: str = '#') -> Tuple[List[str], int]:
    """
    NOTE: use TableReader / MafReader instead of this method!!

    Parse a file with comments in its header to return the comments and the line number to start reader from

    comments, start_line = parse_header_comments(filename)
    with open(portal_file) as fin:
        while start_line > 0:
            next(fin)
            start_line -= 1
        reader = csv.DictReader(fin, delimiter = '\t') # header_line = next(fin)
        portal_lines = [ row for row in reader ]
    """
    comments = []
    start_line = 0
    # find the first line without comments
    with open(filename) as fin:
        for i, line in enumerate(fin):
            if line.startswith(comment_char):
                comments.append(line.strip())
                start_line += 1
    return(comments, start_line)



def is_TERT_promoter(
    mut: Dict,
    gene_key: str = 'Hugo_Symbol',
    start_key: str = 'Start_Position',
    start_ge: int = 1295141, # start pos must be greater than or equal to this
    start_le: int = 1295340 # start pos must be less than or equal to this
    ) -> bool:
    """
    Checks if a variant is in the TERT promoter;

    is_TERT = row['Hugo_Symbol'] == 'TERT'
    pass_TERT_start = int(row['Start_Position']) >= 1295141
    pass_TERT_end = int(row['Start_Position']) <= 1295340
    pass_consequence_or_is_TERT = (pass_consequence_match or (is_TERT and pass_TERT_start and pass_TERT_end))

    NOTE:
    These coordinates are only for B37 genome build

    """
    is_TERT = mut[gene_key] == 'TERT'
    pass_TERT_start = int(mut[start_key]) >= start_ge
    pass_TERT_end = int(mut[start_key]) <= start_le
    mut_is_TERT_promoter = is_TERT and pass_TERT_start and pass_TERT_end
    return(mut_is_TERT_promoter)


#
# CLASSES
#


class TableReader(object):
    """
    Handler for reading a table with comments

    Allows for parsing file attributes and rows without loading the whole file into memory

    NOTE: Input file must have column headers!

    Usage
    -----
    table_reader = TableReader(input_maf_file)
    comment_lines = table_reader.comment_lines
    fieldnames = table_reader.get_fieldnames()
    records = [ rec for rec in table_reader.read() ]


    NOTE: see also
    pluto.tools.TableReader
    pluto.tools.MafWriter
    https://github.com/mskcc/pluto/blob/e10fd75b9f384b8d13ff84f6c955e08b2c354b4f/tools.py#L687

    """
    def __init__(self, filename: str, comment_char: str = '#', delimiter: str = '\t') -> None:
        self.filename = filename
        self.comment_char = comment_char
        self.delimiter = delimiter
        # get the comments from the file and find the beginning of the table header
        self.comments, self.start_line = parse_header_comments(filename, comment_char = self.comment_char)
        self.comment_lines = [ c + '\n' for c in self.comments ]

    def get_reader(self, fin):
        """
        returns the csv.DictReader for the table rows, skipping the comments
        """
        start_line = self.start_line
        # skip comment lines
        while start_line > 0:
            next(fin)
            start_line -= 1
        reader = csv.DictReader(fin, delimiter = self.delimiter)
        return(reader)

    def get_fieldnames(self):
        """
        returns the list of fieldnames for the table
        """
        with open(self.filename,'r') as fin:
            reader = self.get_reader(fin)
            return(reader.fieldnames)

    def read(self):
        """
        iterable to get the record rows from the table, skipping the comments
        """
        with open(self.filename,'r') as fin:
            reader = self.get_reader(fin)
            for row in reader:
                yield(row)

    def count(self):
        """
        Return the total number of records in the table
        """
        num_records = 0
        for _ in self.read():
            num_records += 1
        return(num_records)

class MafReader(TableReader):
    """
    Rename this as a subclass for compatibility; a version of TableReader just for parsing the variants in a maf
    """
    def __init__(self, filename: str, comment_char: str = '#', delimiter: str = '\t') -> None:
        super().__init__(filename, comment_char, delimiter)

class MafWriter(object):
    """
    Class for writing out a .maf format file

    Use this class for applying formatting to mutations and writing them to maf file
    in order to save them to a maf file with specific compatibility requirements

    Use Cases:
    - convert list of mutations to cBioPortal input compatible format

    NOTE: the following scripts / modules have maf formatting logic that needs to be migrated here!
    bin/update_fillout_maf.py
    bin/maf_filter.py
    bin/update_cBioPortal_data.py
    bin/add_af.py
    bin/add_msi_status.py
    bin/maf_col_filter.py
    bin/merge-tables.py
    bin/concat-tables.py

    https://docs.python.org/3/library/csv.html#csv.DictWriter

    NOTE: see also
    pluto.tools.TableReader
    pluto.tools.MafWriter
    https://github.com/mskcc/pluto/blob/e10fd75b9f384b8d13ff84f6c955e08b2c354b4f/tools.py#L687

    Examples:

        reader = MafReader(input_file)
        comments = reader.comments
        fieldnames = reader.get_fieldnames()

        with open(output_file, "w") as fout:
            writer = MafWriter(
                fout = fout,
                fieldnames = fieldnames,
                comments = comments,
                format = "portal")
            for row in reader.read():
                writer.writerow(row)

    """
    def __init__(self,
            fout: TextIO, # an open text-based file handle
            fieldnames: List[str], # list of column headers; will get reformatted based on "format" provided
            comments: List[str] = None, # a list of comment strings to write out in the file header; needs \n appended!
            comments_lines: List[str] = None, # a list of comment lines (with newlines) ready to be printed into the file
            delimiter: str = '\t',
            extrasaction: str = 'ignore', # do not include any fields not in fieldnames; otherwise, 'raise' error if other fields exist
            lineterminator: str = '\n', # avoid issues with carriage returns
            restval: str = "MafWriter.MISSINGVAL", 
            format: str = None, # custom fieldname and output formatter for various compatibility requirements
            ) -> None: # -> csv.DictWriter

        self.fieldnames = fieldnames
        self.comments = comments
        self.comments_lines = comments_lines
        self.format = format
        self.delimiter = delimiter
        self.extrasaction = extrasaction
        self.lineterminator = lineterminator
        self.restval = restval

        # default to empty lists; fill these in based on the format used!
        self.formatted_fieldnames = []
        self.formatted_comments = []

        # check if formatting needs to be applied to fieldnames
        if format == 'portal':
            # set fieldnames and comment lines for portal output
            self.formatted_fieldnames = self.format_portal_fieldnames(fieldnames)
            self.formatted_comments = []
        else:
            # set fieldnames and comment lines for generic maf output
            self.formatted_fieldnames = fieldnames
            if comments_lines:
                self.formatted_comments = comments_lines
            elif comments:
                self.formatted_comments = [ c + '\n' for c in comments ]
            else:
                self.formatted_comments = []

        # write comments if present
        fout.writelines(self.formatted_comments)
        # initialize writer
        self.writer = csv.DictWriter(fout,
            delimiter = self.delimiter,
            fieldnames = self.formatted_fieldnames,
            lineterminator = self.lineterminator,
            extrasaction = self.extrasaction, 
            restval = self.restval)

        # write the header
        self.writer.writeheader()

    def writerow(self, row: Dict, *args, **kwargs) -> None:
        """
        Write out a single row
        """
        # check if row needs formatting update
        if self.format == 'portal':
            row = self.format_portal_row(row)
        self.writer.writerow(row, *args, **kwargs)
    
    @staticmethod
    def format_portal_row(row: Dict) -> Dict:
        """
        Update a maf row for portal output

        NOTE: need to move other maf row updating logic here !!

        """
        # update row keys;
        # "The portal MAF can be minimized since Genome Nexus re-annotates it when HGVSp_Short column is missing"
        if 'HGVSp_Short' in row:
            row['Amino_Acid_Change'] = row['HGVSp_Short']
            row.pop('HGVSp_Short')
        return(row)

    @staticmethod
    def format_portal_fieldnames(fieldnames: List[str]) -> List[str]:
        """
        Reformat the maf columns for compatibility with cBioPortal input
        """
        # make a copy of the initial fieldnames
        portal_fieldnames = [ f for f in fieldnames ]
        
        # rename HGVSp_Short to Amino_Acid_Change
        if 'HGVSp_Short' in portal_fieldnames:
            portal_fieldnames[portal_fieldnames.index('HGVSp_Short')] = 'Amino_Acid_Change'

        # remove any extraneous fieldnames
        portal_fieldnames = [ f for f in portal_fieldnames if f in maf_filter_portal_file_cols_to_keep ]
        return(portal_fieldnames)
