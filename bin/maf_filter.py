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

def filter_row(row, is_impact):
    """
    Check filter criteria against a single row representing a variant
    """
    analysis_keep = False
    portal_keep = False
    fillout_keep = False
    reject_row = True
    reject_reason = None

    # The portal MAF can be minimized since Genome Nexus re-annotates it when HGVSp_Short column is missing
    row['Amino_Acid_Change'] = row['HGVSp_Short']
    event_type = row['Variant_Type']

    # For all events except point mutations, use the variant caller reported allele counts for filtering
    t_depth = int(row['t_depth'])
    t_alt_count = int(row['t_alt_count'])
    if event_type == "SNP":
        t_depth = int(row['fillout_t_depth'])
        t_alt_count = int(row['fillout_t_alt'])

    # check if it is removed by one or more ccs filters and nothing else
    only_ccs_filters = True
    filters = re.split(';|,', row['FILTER'])
    for filter in filters:
        if filter != "mq55" and filter != "nm2" and filter != "asb" and filter != "nad3":
            only_ccs_filters = False
            break

    # some filter criteria to check
    is_not_Pindel = row['set'] != 'Pindel'
    is_impact_and_only_ccs_filters = (is_impact and only_ccs_filters)
    pass_FILTER = row['FILTER'] == 'PASS'
    is_common_variant = row['FILTER'] == 'common_variant'

    # Store all fillout rows
    if row['Mutation_Status'] == 'None':
        fillout_keep = True
        reject_row = False
        return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason)

    # Skip any that failed false-positive filters, except common_variant and Skip all events reported uniquely by Pindel
    if not (( pass_FILTER or is_common_variant or is_impact_and_only_ccs_filters) and is_not_Pindel):
        reject_reason = 'Skip any that failed false-positive filters, except common_variant and Skip all events reported uniquely by Pindel'

    if (pass_FILTER or is_common_variant or is_impact_and_only_ccs_filters) and is_not_Pindel:
        # Skip MuTect-Rescue events for all but IMPACT/HemePACT projects
        if row['set'] == 'MuTect-Rescue' and not is_impact:
            reject_row = True
            reject_reason = 'Skip MuTect-Rescue events for all but IMPACT/HemePACT projects'
            return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason)

        # Skip splice region variants in non-coding genes, or those that are >3bp into introns
        splice_dist = 0
        if re.match(r'splice_region_variant', row['Consequence']) is not None:
            if re.search(r'non_coding_', row['Consequence']) is not None:
                reject_row = True
                reject_reason = 'Skip splice region variants in non-coding genes'
                return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason)

            # Parse the complex HGVSc format to determine the distance from the splice junction
            m = re.match(r'[nc]\.\d+[-+](\d+)_\d+[-+](\d+)|[nc]\.\d+[-+](\d+)', row['HGVSc'])
            if m is not None:
                # For indels, use the closest distance to the nearby splice junction
                splice_dist = min(int(d) for d in [x for x in m.group(1,2,3) if x is not None])
                # print(row['HGVSc'], ';', splice_dist)
                # c.36-3C>T ; 3
                # c.927-3C>G ; 3
                # c.542-4G>T ; 4
                # c.3664-8C>T ; 8
                # c.628-7C>T ; 7
                # c.1705-3C>T ; 3
                if splice_dist > 3:
                    # print(row['HGVSc'], ';', splice_dist)
                    # c.542-4G>T ; 4
                    # c.3664-8C>T ; 8
                    # c.628-7C>T ; 7
                    reject_row = True
                    reject_reason = 'Skip splice region variants that are >3bp into introns'
                    return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason)

        # more filter criteria;
        csq_keep = ['missense_', 'stop_', 'frameshift_', 'splice_', 'inframe_', 'protein_altering_',
            'start_', 'synonymous_', 'coding_sequence_', 'transcript_', 'exon_', 'initiator_codon_',
            'disruptive_inframe_', 'conservative_missense_', 'rare_amino_acid_', 'mature_miRNA_', 'TFBS_']
        csq_pattern = r'|'.join(csq_keep)
        # missense_|stop_|frameshift_|splice_|inframe_|protein_altering_|start_|synonymous_|coding_sequence_|transcript_|exon_|initiator_codon_|disruptive_inframe_|conservative_missense_|rare_amino_acid_|mature_miRNA_|TFBS_
        consequence_match = re.match(csq_pattern, row['Consequence'])
        pass_consequence_match = consequence_match is not None
        is_TERT = row['Hugo_Symbol'] == 'TERT'
        pass_TERT_start = int(row['Start_Position']) >= 1295141
        pass_TERT_end = int(row['Start_Position']) <= 1295340
        pass_consequence_or_is_TERT = (pass_consequence_match or (is_TERT and pass_TERT_start and pass_TERT_end))

        if not pass_consequence_or_is_TERT:
            reject_reason = 'Skip all non-coding events except interesting ones like TERT promoter mutations'

        # Skip all non-coding events except interesting ones like TERT promoter mutations
        if pass_consequence_or_is_TERT:
            # Skip reporting MT muts in IMPACT, and apply the DMP's depth/allele-count/VAF cutoffs as hard filters in IMPACT, and soft filters in non-IMPACT
            if is_impact and row['Chromosome'] == 'MT':
                reject_row = True
                reject_reason = 'Skip reporting MT muts in IMPACT'
                return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason)

            tumor_vaf = float(t_alt_count) / float(t_depth) if t_depth != 0 else 0
            fail_DMP_t_depth = t_depth < 20
            fail_DMP_t_alt_count = t_alt_count < 8
            fail_DMP_tumor_vaf = tumor_vaf < 0.02
            fail_DMP_whitelist_filter = (row['hotspot_whitelist'] == 'FALSE' and (t_alt_count < 10 or tumor_vaf < 0.05))
            if fail_DMP_t_depth or fail_DMP_t_alt_count or fail_DMP_tumor_vaf or fail_DMP_whitelist_filter:
                if is_impact:
                    reject_row = True
                    reject_reason = 'Apply the DMP depth/allele-count/VAF cutoffs as hard filters in IMPACT, and soft filters in non-IMPACT'
                    return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason)

                else:
                    row['FILTER'] = "dmp_filter" if row['FILTER'] == 'PASS' else row['FILTER'] + ";dmp_filter"

            # The portal also skips silent muts, genes without Entrez IDs, and intronic events
            if re.match(r'synonymous_|stop_retained_', row['Consequence']) is None and row['Entrez_Gene_Id'] != 0 and splice_dist <= 2:
                portal_keep = True
                analysis_keep = True
                reject_row = False
                return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason)

            # tag this events in analysis maf as "skipped_by_portal" in column "Mutation_Status"
            else:
                row['Mutation_Status'] = "skipped_by_portal"
                analysis_keep = True
                reject_row = False
                return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason)

    return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason)

def filter_rows(row_list, is_impact, keep_rejects = False):
    """
    Filters the rows in the list
    """
    analysis_keep_list = []
    portal_keep_list = []
    fillout_keep_list = []
    rejected_list = []

    for row in row_list:
        new_row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason = filter_row(row, is_impact)
        if analysis_keep:
            analysis_keep_list.append(row)
        if portal_keep:
            portal_keep_list.append(row)
        if fillout_keep:
            fillout_keep_list.append(row)
        if keep_rejects:
            if reject_row:
                rejected_row = { k:v for k,v in row.items() }
                rejected_row['reject_reason'] = reject_reason
                rejected_list.append(rejected_row)

    return(analysis_keep_list, portal_keep_list, fillout_keep_list, rejected_list)


def main(input_file, version_string, is_impact, analyst_file, portal_file, keep_rejects = False):
    """
    Main control function for the module when called as a script
    """
    version_line = "# Versions: " + version_string.replace('_',' ')

    # get the comments from the file and find the beginning of the table header
    comments, start_line = parse_header_comments(input_file)
    comments.append(version_line)
    comments_lines = [ c + '\n' for c in comments ]

    with open(input_file,'r') as fin:
        # skip comment lines
        while start_line > 0:
            next(fin)
            start_line -= 1

        reader = csv.DictReader(fin, delimiter = '\t')
        fieldnames = reader.fieldnames

        analysis_keep, portal_keep, fillout_keep, rejected_list = filter_rows(row_list = reader, is_impact = is_impact, keep_rejects = keep_rejects)

    # write analysis files
    with open(analyst_file,'w') as fout:
        fout.writelines(comments_lines)
        # ignore fields not in fieldnames
        # NOTE: csv writer includes carriage returns that we dont want
        # https://stackoverflow.com/questions/3191528/csv-in-python-adding-an-extra-carriage-return-on-windows
        writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = fieldnames, extrasaction = 'ignore', lineterminator='\n')
        writer.writeheader()
        for row in analysis_keep:
            writer.writerow(row)

    # write portal file
    # only keep a subset of the fieldnames for the cBioPortal output file
    portal_fieldnames = [ f for f in fieldnames ]
    portal_fieldnames[portal_fieldnames.index('HGVSp_Short')] = 'Amino_Acid_Change'
    portal_fieldnames = [ f for f in portal_fieldnames if f in maf_filter_portal_file_cols_to_keep ]
    with open(portal_file,'w') as fout:
        fout.writelines(comments_lines)
        # ignore fields not in fieldnames
        writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = portal_fieldnames, extrasaction = 'ignore', lineterminator='\n')
        writer.writeheader()
        for row in portal_keep:
            writer.writerow(row)
        # write fillout if available
        for row in fillout_keep:
            writer.writerow(row)

    # save a copy of the rows that were rejected with their rejection reasons
    if keep_rejects:
        with open("rejected.tsv", "w") as fout:
            writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = [ *fieldnames, 'reject_reason'], extrasaction = 'ignore', lineterminator='\n')
            writer.writeheader()
            for row in rejected_list:
                writer.writerow(row)

def parse():
    """
    Parse the CLI args

    maf_filter2.py Proj_08390_G.muts.maf 2.x True analyst_file3.tsv portal_file3.tsv
    """
    input_file = sys.argv[1]
    version_string = sys.argv[2]
    is_impact = True if sys.argv[3]=='True' else False
    analyst_file = sys.argv[4]
    portal_file = sys.argv[5]

    # add secret positional arg for saving the rejected variants in a separate file
    if len(sys.argv) > 6:
        keep_rejects = True
    else:
        keep_rejects = False

    main(input_file, version_string, is_impact, analyst_file, portal_file, keep_rejects)

if __name__ == '__main__':
    parse()
