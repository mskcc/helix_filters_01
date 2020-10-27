#!/usr/bin/env python3
import argparse,csv
from cBioPortal_utils import parse_header_comments

def load_IMPACT_data(filename):
    """
    load the regions from the IMPACT targets file into a dict of type
    { chrom: [1, 2, ..., n], ... }
    for each Chromosome and all covered positions in the file
    """
    d={}
    with open(filename,'r') as f:
        for line in f:
            if not line.startswith('@'): # skip header lines in the file
                line=line.rstrip().split()
                chr=line[0]
                spos=int(line[1])
                epos=int(line[2])
                range_l=range(spos,epos+1) # expand the start and stop positions into a list of ints for each position
                if chr not in d:
                    d[chr]=[] # each chrom starts with a list to hold values
                d[chr]+=range_l # append new range values to the chrom position entries list
    return d

def is_in_IMPACT(chr,pos,IMPACT_d):
    position_present = False # start False by default
    try:
        position_present = str(pos in IMPACT_d[chr])
    except KeyError: # chrom not in the IMPACT list
        pass # do nothing because False is the default value
    return(position_present)


def parse_CLI_args():
    """
    Parse the CLI args
    add_is_in_impact.py Proj_08390_G.muts.maf IMPACT468_b37_targets.bed
    """
    parser = argparse.ArgumentParser(description = 'Script for adding if mutation is in IMPACT panel')
    parser.add_argument('--input_file',    dest = 'input_file',          required = True,                     help='Input maf filename')
    parser.add_argument('--output_file',   dest = 'output_file',         required = False, default='default', help='Output maf filename')
    parser.add_argument('--IMPACT_file',   dest = 'IMPACT_target_files', required = True,                     help='IMPACT file to use')

    args = parser.parse_args()

    if args.output_file=='default':
        args.output_file=args.input_file.split('/')[-1].split('.')[0]+'_is_in_IMPACT_added.maf'

    return args


def main():
    args=parse_CLI_args()

    IMPACT_d=load_IMPACT_data(args.IMPACT_target_files)

    # get the comments from the file and find the beginning of the table header
    comments, start_line = parse_header_comments(args.input_file)
    comments_lines = [ c + '\n' for c in comments ]

    is_in_impact_added_output=[]
    with open(args.input_file,'r') as fin:
        # skip comment lines
        while start_line > 0:
            next(fin)
            start_line -= 1

        reader = csv.DictReader(fin, delimiter = '\t')
        fieldnames = reader.fieldnames
        fieldnames.append('is_in_impact')
        for row in reader:
            row['is_in_impact']=is_in_IMPACT(row['Chromosome'],int(row['Start_Position']),IMPACT_d)
            is_in_impact_added_output.append(row)

    # write analysis files
    with open(args.output_file,'w') as fout:
        fout.writelines(comments_lines)
        # ignore fields not in fieldnames
        # NOTE: csv writer includes carriage returns that we dont want
        # https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
        writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = fieldnames, extrasaction = 'ignore', lineterminator='\n')
        writer.writeheader()
        for row in is_in_impact_added_output:
            writer.writerow(row)

if __name__ == '__main__':
    main()
