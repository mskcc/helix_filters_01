#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to update mutation file with extra columns for cBioPortal

Description
-----------

Additional columns for portal/sample_data_clinical.txt

These can be found from a facets file that looks like this:
s_C_ABDC_N001_d__s_C_ABDC_R002_d.txt

Example path:
/juno/work/ci/songt/custom_analysis/test_06287_BF/facets/s_C_ABDC_N001_d__s_C_ABDC_R002_d/s_C_ABDC_N001_d__s_C_ABDC_R002_d.txt


You must only use the row that says “hisens” from the column run_type.

The columns that need to be grabbed are:
purity
ploidy
facets_version
genome_doubled

However they should be renamed and appended to portal/sample_data_clinical.txt
purity = ASCN_PURITY
ploidy = ASCN_PLOIDY
facets_version = ASCN_VERSION
genome_doubled = ASCN_WGD   *Note. Convert “False” to “no WGD” and convert “True” to “WGD”

---

Additional columns for portal/data_mutations_extended.txt
These can be found from the mutation mafs after they have been run through facets maf annotator.

Example path:
/juno/work/ci/songt/custom_analysis/test_06287_BF/facets/test_06287_BF/maf/s_C_ABDC_R002_d.s_C_ABDC_N001_d.muts.ccf.maf

The columns that need to be grabbed are:
tcn
lcn
expected_alt_copies
ccf_expected_copies
ccf_expected_copies_lower
ccf_expected_copies_upper

However they should be renamed as:
tcn = ASCN.TOTAL_COPY_NUMBER
lcn = ASCN.MINOR_COPY_NUMBER
expected_alt_copies = ASCN.EXPECTED_ALT_COPIES
ccf_expected_copies = ASCN.CCF_EXPECTED_COPIES
ccf_expected_copies_lower = ASCN.CCF_EXPECTED_COPIES_LOWER
ccf_expected_copies_upper = ASCN.CCF_EXPECTED_COPIES_UPPER

Two additional columns must be added based on existing information:
ASCN.ASCN_METHOD
ASCN.ASCN_INTEGER_COPY_NUMBER

All other facets related columns generated by maf annotator are not used by portal and can be dropped.

The value for ASCN.ASCN_METHOD will always be “FACETS”

The value for ASCN.ASCN_INTEGER_COPY_NUMBER can be calculated by using WGD (genome_doubled from the data clinical or facets .txt file),  mcn, and lcn and doing a key look up based on the dictionary below.
 The mcn is calculated by int(tcn) - int(lcn)

Example.
ASCN_WGD = “no WGD”
tcn = 3
lcn = 1
mcn = tcn - lcn = 2

Using the wgdfalsedict below.. wgdfalsedict[(2,1)] = 1

ASCN.ASCN_INTEGER_COPY_NUMBER will equal 1

Facets documentation for the value:
https://github.com/mskcc/facets-suite/blob/f2b3a46ef00085fd56c693536f66992c691809be/data-raw/sysdata.R#L174

Usage
-----

$ update_cBioPortal_data.py sample --input output/portal/data_clinical_sample.txt --facets-txt output/facets-suite/s_C_ABCDE_P001_d.s_C_ABCDE_N001_d.txt --output foo.txt

$ bin/update_cBioPortal_data.py mutations --input data_mutations.cc.maf --facets-txt facets-data.txt --output bar.txt

"""
import csv
import sys
import argparse

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .cBioPortal_utils import create_file_lines
    from .cBioPortal_utils import update_sample_data
    from .cBioPortal_utils import sample_data_remove_cols
    from .cBioPortal_utils import facets_data_keep_cols_map
    from .cBioPortal_utils import parse_facets_data

if __name__ == "__main__":
    from cBioPortal_utils import create_file_lines
    from cBioPortal_utils import update_sample_data
    from cBioPortal_utils import sample_data_remove_cols
    from cBioPortal_utils import facets_data_keep_cols_map
    from cBioPortal_utils import parse_facets_data

# # remove these columns from data_clinical_sample.txt data while updating it with Facets Suite data
# sample_data_remove_cols = ["purity", "ploidy", "facets_version"]
mutation_data_keep_cols_map = {
    "tcn": "ASCN.TOTAL_COPY_NUMBER",
    "lcn": "ASCN.MINOR_COPY_NUMBER",
    "expected_alt_copies": "ASCN.EXPECTED_ALT_COPIES",
    "ccf_expected_copies": "ASCN.CCF_EXPECTED_COPIES",
    "ccf_expected_copies_lower": "ASCN.CCF_EXPECTED_COPIES_LOWER",
    "ccf_expected_copies_upper": "ASCN.CCF_EXPECTED_COPIES_UPPER"
}

# https://github.com/mskcc/facets-suite/blob/f2b3a46ef00085fd56c693536f66992c691809be/data-raw/sysdata.R#L174
# (wgd, mcn, lcn): numeric_call
facets_call_states = {
('TRUE', 0,0):-2,
('TRUE', 1,0):-1,
('TRUE', 2,0):-1,
('TRUE', 3,0):-1,
('TRUE', 4,0):-1,
('TRUE', 5,0):1,
('TRUE', 6,0):2,
('TRUE', 1,1):-1,
('TRUE', 2,1):-1,
('TRUE', 3,1):-1,
('TRUE', 4,1):1,
('TRUE', 5,1):2,
('TRUE', 6,1):2,
('TRUE', 2,2):0,
('TRUE', 3,2):1,
('TRUE', 4,2):2,
('TRUE', 5,2):2,
('TRUE', 6,2):2,
('TRUE', 3,3):2,
('TRUE', 4,3):2,
('TRUE', 5,3):2,
('TRUE', 6,3):2,
('FALSE', 0,0):-2,
('FALSE', 1,0):-1,
('FALSE', 2,0):-1,
('FALSE', 3,0):1,
('FALSE', 4,0):1,
('FALSE', 5,0):2,
('FALSE', 6,0):2,
('FALSE', 1,1):0,
('FALSE', 2,1):1,
('FALSE', 3,1):1,
('FALSE', 4,1):2,
('FALSE', 5,1):2,
('FALSE', 6,1):2,
('FALSE', 2,2):1,
('FALSE', 3,2):2,
('FALSE', 4,2):2,
('FALSE', 5,2):2,
('FALSE', 6,2):2,
('FALSE', 3,3):2,
('FALSE', 4,3):2,
('FALSE', 5,3):2,
('FALSE', 6,3):2,
}

def update_mutation_data(mut_data, facets_data = None, sample_id = None):
    """
    """
    # try to get a sample ID from the mutation data if it was not passed
    if sample_id == None:
        # prefer to use 'tumor' field, otherwise use 'sample' field
        if 'tumor' in mut_data:
            sample_id = mut_data['tumor']
        elif 'sample' in mut_data:
            sample_id = mut_data['sample']

    # copy the original dict
    d = { k:v for k,v in mut_data.items() }

    # add new columns that match the old columns
    for old_key, new_key in mutation_data_keep_cols_map.items():
        if old_key in d:
            d[new_key] = d[old_key]
    d['ASCN.ASCN_METHOD'] = 'FACETS'

    # match against Facets data if present
    if facets_data == None:
        d['ASCN.ASCN_INTEGER_COPY_NUMBER'] = 'NA'
    else:
        # need a sample ID to look up the facets
        if sample_id == None:
            d['ASCN.ASCN_INTEGER_COPY_NUMBER'] = 'NA'
        else:
            # calculate the ASCN.ASCN_INTEGER_COPY_NUMBER value
            try:
                wgd = facets_data[sample_id]['genome_doubled'] # 'TRUE' or 'FALSE'
                tcn = int(d['tcn'])
                lcn = int(d['lcn'])
                mcn = tcn - lcn
                numeric_call = str(facets_call_states[(wgd, mcn, lcn)])
                d['ASCN.ASCN_INTEGER_COPY_NUMBER'] = numeric_call
            except (ValueError, KeyError):
                d['ASCN.ASCN_INTEGER_COPY_NUMBER'] = 'NA'
    return(d)

def update_sample_file(**kwargs):
    """
    Update the data_clinical_sample.txt file with the new Facets Suite data
    """
    input_file = kwargs.pop('input_file')
    output_file = kwargs.pop('output_file')
    facets_txt_file = kwargs.pop('facets_txt_file')

    # LOAD ALL SAMPLE DATA
    all_sample_data = []

    # need to find the row to start reading from
    skip_row = 0
    with open(input_file) as fin:
        for i, line in enumerate(fin):
            if line.startswith('#'):
                skip_row += 1

    # skip all '#' comment rows in header and load all the data
    with open(input_file) as fin:
        while skip_row > 0:
            next(fin)
            skip_row -= 1
        reader = csv.DictReader(fin, delimiter = '\t')
        for row in reader:
            all_sample_data.append(row)

    # LOAD ALL FACETS DATA
    all_facets_data = []
    with open(facets_txt_file) as fin:
        reader = csv.DictReader(fin, delimiter = '\t')
        for row in reader:
            all_facets_data.append(row)

    # clean up the facets data to remove stuff we dont want and recalculate things
    parsed_facets_data = parse_facets_data(all_facets_data)

    # update all the sample datas based on facets data
    updated_sample_data = []
    for sample_data in all_sample_data:
        new_sample_data = update_sample_data(sample_data, facets_data = parsed_facets_data)
        updated_sample_data.append(new_sample_data)

    # create the lines to output to the file
    lines = create_file_lines(updated_sample_data)

    # write all the lines to file
    with open(output_file, "w") as fout:
        fout.writelines(lines)


def update_mutations_file(**kwargs):
    """
    Update the data_mutations_extended.txt file with the Facets data saved to the updated data_clinical_sample.txt file
    """
    input_file = kwargs.pop('input_file')
    output_file = kwargs.pop('output_file')
    facets_txt_file = kwargs.pop('facets_txt_file')

    # LOAD ALL FACETS DATA
    all_facets_data = []
    with open(facets_txt_file) as fin:
        reader = csv.DictReader(fin, delimiter = '\t')
        for row in reader:
            all_facets_data.append(row)

    # clean up the facets data to remove stuff we dont want and recalculate things
    parsed_facets_data = parse_facets_data(all_facets_data)

    # UPDATE ALL THE MUTATIONS DATA
    with open(input_file) as fin, open(output_file, "w") as fout:
        reader = csv.DictReader(fin, delimiter = '\t')

        # need to update the first row in order to know what fieldnames to output
        first_row = next(reader)
        updated_first_row = update_mutation_data(mut_data = first_row, facets_data = parsed_facets_data)
        fieldnames = updated_first_row.keys()

        # set up the output file
        writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = fieldnames)
        writer.writeheader()
        writer.writerow(updated_first_row)

        # update all the rows and write them out
        for row in reader:
            updated_row = update_mutation_data(mut_data = row, facets_data = parsed_facets_data)
            writer.writerow(updated_row)

def main():
    """
    Parse command line arguments to run the script
    """
    # top level CLI arg parser; args common to all output files go here
    parser = argparse.ArgumentParser(description = 'Update mutation file with extra columns for cBioPortal')

    # add sub-parsers for specific file outputs
    subparsers = parser.add_subparsers(help ='Sub-commands available')

    # update the data_clinical_sample.txt file
    sample = subparsers.add_parser('sample', help = 'Update the clinical sample data file')
    sample.add_argument('--input', dest = 'input_file', required = True, help = 'Path to the data_clinical_sample.txt input file')
    sample.add_argument('--output', dest = 'output_file', required = True, help = 'Name of the output file')
    sample.add_argument('--facets-txt', dest = 'facets_txt_file', required = True, help = 'The .txt output from Facets Suite')
    sample.set_defaults(func = update_sample_file)

    mutations = subparsers.add_parser('mutations', help = 'Update the clinical mutations data file')
    mutations.add_argument('--input', dest = 'input_file', required = True, help = 'Name of the input file')
    mutations.add_argument('--output', dest = 'output_file', required = True, help = 'Name of the output file')
    mutations.add_argument('--facets-txt', dest = 'facets_txt_file', required = True, help = 'The .txt output from Facets Suite')
    mutations.set_defaults(func = update_mutations_file)

    args = parser.parse_args()
    args.func(**vars(args))

if __name__ == '__main__':
    main()