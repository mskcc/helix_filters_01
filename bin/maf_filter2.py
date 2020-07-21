#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for filtering maf data for use with analysis and cBioPortal

derived from:
https://github.com/mskcc/roslin-variant/blob/2d0f7f7b78b89bb31f5bf8b8eb678fd41998213b/setup/bin/maf_filter.py
"""
import sys
import os
import csv
import re

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .cBioPortal_utils import maf_filter_portal_file_cols_to_keep
    from .cBioPortal_utils import parse_header_comments

if __name__ == "__main__":
    from cBioPortal_utils import maf_filter_portal_file_cols_to_keep
    from cBioPortal_utils import parse_header_comments

input_file = sys.argv[1]
roslin_version_string = sys.argv[2]
is_impact = True if sys.argv[3]=='True' else False
analyst_file = sys.argv[4]
portal_file = sys.argv[5]
roslin_version_line = "# Versions: " + roslin_version_string.replace('_',' ')

# Read input maf file
fillout_keep = []
analysis_keep = []
portal_keep = []


# get the comments from the file and find the beginning of the table header
comments, start_line = parse_header_comments(input_file)
comments.append(roslin_version_line)
comments = [ c + '\n' for c in comments ]

with open(input_file,'r') as fin:

    # skip comment lines
    while start_line > 0:
        next(fin)
        start_line -= 1

    reader = csv.DictReader(fin, delimiter = '\t')
    fieldnames = reader.fieldnames

    for row in reader:
        # The portal MAF can be minimized since Genome Nexus re-annotates it when HGVSp_Short column is missing
        # header[header.index('HGVSp_Short')] = 'Amino_Acid_Change'
        row['Amino_Acid_Change'] = row['HGVSp_Short']
        event_type = row['Variant_Type']
        # For all events except point mutations, use the variant caller reported allele counts for filtering
        tdp = int(row['t_depth'])
        tad = int(row['t_alt_count'])
        if event_type == "SNP":
            tdp = int(row['fillout_t_depth'])
            tad = int(row['fillout_t_alt'])
        # check if it is removed by one or more ccs filters and nothing else
        only_ccs_filters = True
        filters = re.split(';|,', row['FILTER'])
        for filter in filters:
            if filter != "mq55" and filter != "nm2" and filter != "asb" and filter != "nad3":
                only_ccs_filters = False
                break
        arr_key = [row['Chromosome'], row['Start_Position'], row['Reference_Allele'], row['Tumor_Seq_Allele2']]
        key = '\t'.join(arr_key)
        # Store all fillout rows first
        # Skip any that failed false-positive filters, except common_variant and Skip all events reported uniquely by Pindel
        if row['Mutation_Status'] == 'None':
            fillout_keep.append(row)
        elif (row['FILTER'] == 'PASS' or row['FILTER'] == 'common_variant' or (is_impact and only_ccs_filters)) and row['set'] != 'Pindel':
            # Skip MuTect-Rescue events for all but IMPACT/HemePACT projects
            if row['set'] == 'MuTect-Rescue' and not is_impact:
                continue
            # Skip splice region variants in non-coding genes, or those that are >3bp into introns
            splice_dist = 0
            if re.match(r'splice_region_variant', row['Consequence']) is not None:
                if re.search(r'non_coding_', row['Consequence']) is not None:
                    continue
                # Parse the complex HGVSc format to determine the distance from the splice junction
                m = re.match(r'[nc]\.\d+[-+](\d+)_\d+[-+](\d+)|[nc]\.\d+[-+](\d+)', row['HGVSc'])
                if m is not None:
                    # For indels, use the closest distance to the nearby splice junction
                    splice_dist = min(int(d) for d in [x for x in m.group(1,2,3) if x is not None])
                    if splice_dist > 3:
                        continue
            # Skip all non-coding events except interesting ones like TERT promoter mutations
            csq_keep = ['missense_', 'stop_', 'frameshift_', 'splice_', 'inframe_', 'protein_altering_',
                'start_', 'synonymous_', 'coding_sequence_', 'transcript_', 'exon_', 'initiator_codon_',
                'disruptive_inframe_', 'conservative_missense_', 'rare_amino_acid_', 'mature_miRNA_', 'TFBS_']
            if re.match(r'|'.join(csq_keep), row['Consequence']) is not None or (row['Hugo_Symbol'] == 'TERT' and int(row['Start_Position']) >= 1295141 and int(row['Start_Position']) <= 1295340):
                # Skip reporting MT muts in IMPACT, and apply the DMP's depth/allele-count/VAF cutoffs as hard filters in IMPACT, and soft filters in non-IMPACT
                if is_impact and row['Chromosome'] == 'MT':
                    continue
                tumor_vaf = float(tad) / float(tdp) if tdp != 0 else 0
                if tdp < 20 or tad < 8 or tumor_vaf < 0.02 or (row['hotspot_whitelist'] == 'FALSE' and (tad < 10 or tumor_vaf < 0.05)):
                    if is_impact:
                        continue
                    else:
                        row['FILTER'] = "dmp_filter" if row['FILTER'] == 'PASS' else row['FILTER'] + ";dmp_filter"
                # The portal also skips silent muts, genes without Entrez IDs, and intronic events
                if re.match(r'synonymous_|stop_retained_', row['Consequence']) is None and row['Entrez_Gene_Id'] != 0 and splice_dist <= 2:
                    portal_keep.append(row)
                    analysis_keep.append(row)
                # tag this events in analysis maf as "skipped_by_portal" in column "Mutation_Status"
                else:
                    row['Mutation_Status'] = "skipped_by_portal"
                    analysis_keep.append(row)


# write into analysis files
# NOTE: csv writer includes carriage returns
# https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
with open(analyst_file,'w') as fout:
    fout.writelines(comments)
    # ignore fields not in fieldnames
    writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = fieldnames, extrasaction = 'ignore', lineterminator='\n')
    writer.writeheader()
    for row in analysis_keep:
        writer.writerow(row)

# write portal file
# only keep a subset of the fieldnames for the cBioPortal output file
with open(portal_file,'w') as fout:
    fout.writelines(comments)
    # ignore fields not in fieldnames
    writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = maf_filter_portal_file_cols_to_keep, extrasaction = 'ignore', lineterminator='\n')
    writer.writeheader()
    for row in portal_keep:
        writer.writerow(row)
    # write fillout if available
    for row in fillout_keep:
        writer.writerow(row)
