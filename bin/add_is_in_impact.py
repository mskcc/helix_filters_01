#!/usr/bin/env python3
"""
-----
NOTE: MOVE MAF OUTPUT AND FORMATTER TO cBioPortal_utils.MafWriter !! DO NOT ADD MORE ONE-OFF MAF FORMATTING MODULES AND METHODS !!
-----
"""
import argparse,csv
from cBioPortal_utils import MafReader

def load_IMPACT_data(filename, delimiter = '\t'):
    """
    load the IMPACT genes from a file

    file format;
        <gene_label>\t<assay_label>
        TP53\tImpact468
    """
    genes = {}
    with open(filename) as f:
        # read the gene from the value in the first column in the file
        for line in f:
            parts = line.split(delimiter)
            gene_label = parts[0].strip()

            # initialize set of assays so we dont accumulate duplicates
            if gene_label not in genes:
                genes[gene_label] = set()

            if len(parts) > 1: # line has gene and assay label
                assay_label = parts[1].strip()
                genes[gene_label].add(assay_label)
            else:
                genes[gene_label].add('')
    return(genes)

def is_in_IMPACT(gene, IMPACT_genes_l, NA_str = '.'):
    """
    Check if the gene is in the IMPACT gene set

    IMPACT_genes_l is a dict of sets;

    {
    'TP53': set(['IMPACT505', 'Impact468']),
    }
    """
    present_in_set = False # start false by default
    assays = NA_str # default value for no assay's present

    present_in_set = gene in IMPACT_genes_l

    if present_in_set:
        assays = ','.join(sorted(IMPACT_genes_l[gene])) # comma-delimited string of all the assays for the gene
    return(present_in_set, assays)


def parse_CLI_args():
    """
    Parse the CLI args
    add_is_in_impact.py Proj_08390_G.muts.maf IMPACT468_b37_targets.bed
    """
    parser = argparse.ArgumentParser(description = 'Script for adding if mutation is in IMPACT panel')
    parser.add_argument('--input_file',    dest = 'input_file',          required = True,                     help='Input maf filename')
    parser.add_argument('--output_file',   dest = 'output_file',         required = False, default='default', help='Output maf filename')
    parser.add_argument('--IMPACT_file',   dest = 'IMPACT_genes_files', required = True,                     help='IMPACT file to use')
    parser.add_argument('--include-assay', dest = 'include_assay', action="store_true", help='Include the assay labels for matches (IMPACT file must have assay labels in second column)')

    args = parser.parse_args()

    if args.output_file=='default':
        args.output_file=args.input_file.split('/')[-1].split('.')[0]+'_is_in_IMPACT_added.maf'

    return args


def main():
    args=parse_CLI_args()
    include_assay = args.include_assay # store_true; False by default

    IMPACT_genes_l=load_IMPACT_data(args.IMPACT_genes_files)

    is_in_impact_added_output=[]

    # parser for the input maf file
    maf_reader = MafReader(args.input_file)

    # write analysis files
    with open(args.output_file,'w') as fout:

        # load comments and columns labels from the input maf
        comment_lines = maf_reader.comment_lines
        fieldnames = maf_reader.get_fieldnames()

        # add the new columns labels for output
        fieldnames.append('is_in_impact')
        if include_assay:
            fieldnames.append('impact_assays')

            # is_in_impact_added_output.append(row)

        # write the comments back to the output
        fout.writelines(comment_lines)

        # start output csv parser
        # ignore fields not in fieldnames
        # NOTE: csv writer includes carriage returns that we dont want
        # https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
        writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = fieldnames, extrasaction = 'ignore', lineterminator='\n')
        writer.writeheader()

        # update each input row and write it to output
        for row in maf_reader.read():
            present_in_set, assays = is_in_IMPACT(row['Hugo_Symbol'],IMPACT_genes_l)
            row['is_in_impact'] = present_in_set
            if include_assay:
                row['impact_assays'] = assays
            writer.writerow(row)

if __name__ == '__main__':
    main()
