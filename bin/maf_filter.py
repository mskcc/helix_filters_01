#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script for filtering maf data for use with analysis and cBioPortal

derived from:
https://github.com/mskcc/roslin-variant/blob/2d0f7f7b78b89bb31f5bf8b8eb678fd41998213b/setup/bin/maf_filter.py

-----
NOTE: MOVE MAF OUTPUT AND FORMATTER TO cBioPortal_utils.MafWriter !! DO NOT ADD MORE ONE-OFF MAF FORMATTING MODULES AND METHODS !!
-----
"""
import sys
import os
import csv
import re
import argparse
import json
from typing import Dict, Tuple, List

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .cBioPortal_utils import maf_filter_portal_file_cols_to_keep
    from .cBioPortal_utils import parse_header_comments

if __name__ == "__main__":
    from cBioPortal_utils import maf_filter_portal_file_cols_to_keep
    from cBioPortal_utils import parse_header_comments

def filter_row(row: Dict, is_impact: bool) -> Tuple[Dict, bool, bool, bool, bool, str]:
    """
    Check filter criteria against a single row representing a variant

    Parameters
    ----------
    row: dict
        a dictionary representing a single row read in from a .maf file
    is_impact: bool
        wether the sample should be assumed to be IMPACT sample or not; adjusted filter criteria

    Returns
    -------
    dict:
        the original row that was passed into the filter function (row)
    bool:
        whether the row should be kept in the "analysis" output file (analysis_keep)
    bool:
        whether the row should be kept in the cBioPortal output file (portal_keep)
    bool:
        whether the row should be kept as a fillout row in the cBioPortal file (fillout_keep)
    bool:
        whether the row should be rejected (reject_row)
    str|None:
        the reason the row was rejected (reject_reason)
    """
    # flags to determine whether the row should be kept or rejected
    analysis_keep = False
    portal_keep = False
    fillout_keep = False
    reject_row = True
    reject_reason = None
    reject_flag = None

    # dict to hold the filter criteria we are testing against
    filter_flags = {}

    # update row keys;
    # "The portal MAF can be minimized since Genome Nexus re-annotates it when HGVSp_Short column is missing"
    row['Amino_Acid_Change'] = row['HGVSp_Short']
    # NOTE: !!! This ^^^ logic is now in cBioProtal_utils.MafWriter ; from now on get this functionality from there!!
    
    event_type = row['Variant_Type']

    # get some values from the row to use for filter criteria
    # For all events except point mutations, use the variant caller reported allele counts for filtering
    t_depth = int(row['t_depth'])
    t_alt_count = int(row['t_alt_count'])
    if event_type == "SNP":
        t_depth = int(row['fillout_t_depth'])
        t_alt_count = int(row['fillout_t_alt'])
    tumor_vaf = float(t_alt_count) / float(t_depth) if t_depth != 0 else 0

    # check if it is removed by one or more ccs filters and nothing else
    only_ccs_filters = True
    filters = re.split(';|,', row['FILTER'])
    for filter in filters:
        if filter != "mq55" and filter != "nm2" and filter != "asb" and filter != "nad3":
            only_ccs_filters = False
            break

    HGVSc_splice_match = re.match(r'[nc]\.\d+[-+](\d+)_\d+[-+](\d+)|[nc]\.\d+[-+](\d+)', row['HGVSc']) # c.36-3C>T ; 3

    # some filter criteria to check
    is_not_Pindel = row['set'] != 'Pindel'
    is_impact_and_only_ccs_filters = (is_impact and only_ccs_filters)
    pass_FILTER = row['FILTER'] == 'PASS'
    is_common_variant = row['FILTER'] == 'common_variant'
    Mutation_Status_None = row['Mutation_Status'] == 'None'

    # Skip any that failed false-positive filters, except common_variant and Skip all events reported uniquely by Pindel
    pass_FILTER_or_is_common_variant_or_is_common_variant_and_is_not_Pindel = (pass_FILTER or is_common_variant or is_impact_and_only_ccs_filters) and is_not_Pindel

    # Skip MuTect-Rescue events for all but IMPACT/HemePACT projects
    set_MuTect_Rescue = row['set'] == 'MuTect-Rescue'
    set_MuTect_Rescue_and_not_is_impact =  set_MuTect_Rescue and not is_impact
    splice_region_variant_with_Consequence = re.match(r'splice_region_variant', row['Consequence']) is not None
    non_coding_with_Consequence = re.search(r'non_coding_', row['Consequence']) is not None

    splice_dist = 0
    HGVSc_splice_match_is_not_None = HGVSc_splice_match is not None
    if HGVSc_splice_match_is_not_None:
        # For indels, use the closest distance to the nearby splice junction
        splice_dist = min(int(d) for d in [x for x in HGVSc_splice_match.group(1,2,3) if x is not None])
        # c.36-3C>T ; 3
        # c.927-3C>G ; 3
        # c.542-4G>T ; 4
        # c.3664-8C>T ; 8
        # c.628-7C>T ; 7
        # c.1705-3C>T ; 3
    splice_dist_min_pass = splice_dist > 3
    # c.542-4G>T ; 4
    # c.3664-8C>T ; 8
    # c.628-7C>T ; 7

    consequence_keep = ['missense_', 'stop_', 'frameshift_', 'splice_', 'inframe_', 'protein_altering_',
        'start_', 'synonymous_', 'coding_sequence_', 'transcript_', 'exon_', 'initiator_codon_',
        'disruptive_inframe_', 'conservative_missense_', 'rare_amino_acid_', 'mature_miRNA_', 'TFBS_']
    consequence_pattern = r'|'.join(consequence_keep) # missense_|stop_|frameshift_|splice_|inframe_|protein_altering_|start_|synonymous_|coding_sequence_|transcript_|exon_|initiator_codon_|disruptive_inframe_|conservative_missense_|rare_amino_acid_|mature_miRNA_|TFBS_
    consequence_match = re.match(consequence_pattern, row['Consequence'])

    pass_consequence_match = consequence_match is not None
    is_TERT = row['Hugo_Symbol'] == 'TERT'
    pass_TERT_start = int(row['Start_Position']) >= 1295141
    pass_TERT_end = int(row['Start_Position']) <= 1295340
    pass_consequence_or_is_TERT = (pass_consequence_match or (is_TERT and pass_TERT_start and pass_TERT_end))
    is_impact_and_is_MT = is_impact and row['Chromosome'] == 'MT'
    fail_DMP_t_depth = t_depth < 20
    fail_DMP_t_alt_count = t_alt_count < 8
    fail_DMP_tumor_vaf = tumor_vaf < 0.02
    fail_DMP_whitelist_filter = (row['hotspot_whitelist'] == 'FALSE' and (t_alt_count < 10 or tumor_vaf < 0.05))
    dmp_fail = fail_DMP_t_depth or fail_DMP_t_alt_count or fail_DMP_tumor_vaf or fail_DMP_whitelist_filter
    dmp_fail_and_is_impact = dmp_fail and is_impact

    # NOTE: why are we changing the column value here???
    if dmp_fail and not dmp_fail_and_is_impact:
        row['FILTER'] = "dmp_filter" if row['FILTER'] == 'PASS' else row['FILTER'] + ";dmp_filter"

    synonymous_match = re.match(r'synonymous_|stop_retained_', row['Consequence']) is None
    entrez_gene_id_0 = row['Entrez_Gene_Id'] != 0
    intronic_event = splice_dist <= 2
    silent_mut_no_entrez_intronic = synonymous_match and entrez_gene_id_0 and intronic_event

    # analysis_and_portal_pass = pass_FILTER_or_is_common_variant_or_is_common_variant_and_is_not_Pindel \
    #     and pass_consequence_or_is_TERT \
    #     and silent_mut_no_entrez_intronic
    #
    # analysis_pass = pass_FILTER_or_is_common_variant_or_is_common_variant_and_is_not_Pindel \
    # and not set_MuTect_Rescue_and_not_is_impact \
    # and not splice_region_variant_with_Consequence \
    # and pass_consequence_or_is_TERT \
    # and not is_impact_and_is_MT \
    # and not dmp_fail_and_is_impact \
    # and silent_mut_no_entrez_intronic

    filter_flags["silent_mut_no_entrez_intronic"] = silent_mut_no_entrez_intronic
    filter_flags["intronic_event"] = intronic_event
    filter_flags["entrez_gene_id_0"] = entrez_gene_id_0
    filter_flags["synonymous_match"] = synonymous_match
    filter_flags["tumor_vaf"] = tumor_vaf
    filter_flags["is_not_Pindel"] = is_not_Pindel
    filter_flags["is_impact"] = is_impact
    filter_flags["only_ccs_filters"] = only_ccs_filters
    filter_flags["is_impact_and_only_ccs_filters"] = is_impact_and_only_ccs_filters
    filter_flags["pass_FILTER"] = pass_FILTER
    filter_flags["is_common_variant"] = is_common_variant
    filter_flags["Mutation_Status_None"] = Mutation_Status_None
    filter_flags["pass_FILTER_or_is_common_variant_or_is_common_variant_and_is_not_Pindel"] = pass_FILTER_or_is_common_variant_or_is_common_variant_and_is_not_Pindel
    filter_flags["set_MuTect_Rescue_and_not_is_impact"] = set_MuTect_Rescue_and_not_is_impact
    # Skip splice region variants in non-coding genes, or those that are >3bp into introns
    filter_flags["splice_region_variant_with_Consequence"] = splice_region_variant_with_Consequence
    filter_flags["non_coding_with_Consequence"] = non_coding_with_Consequence
    filter_flags["HGVSc_splice_match_is_not_None"] = HGVSc_splice_match_is_not_None
    filter_flags["pass_consequence_match"] = pass_consequence_match
    filter_flags["is_TERT"] = is_TERT
    filter_flags["pass_TERT_start"] = pass_TERT_start
    filter_flags["pass_TERT_end"] = pass_TERT_end
    filter_flags["pass_consequence_or_is_TERT"] = pass_consequence_or_is_TERT
    filter_flags["is_impact_and_is_MT"] = is_impact_and_is_MT
    filter_flags["fail_DMP_t_depth"] = fail_DMP_t_depth
    filter_flags["fail_DMP_t_alt_count"] = fail_DMP_t_alt_count
    filter_flags["fail_DMP_tumor_vaf"] = fail_DMP_tumor_vaf
    filter_flags["fail_DMP_whitelist_filter"] = fail_DMP_whitelist_filter
    filter_flags["dmp_fail"] = dmp_fail
    filter_flags["dmp_fail_and_is_impact"] = dmp_fail_and_is_impact
    filter_flags["splice_dist"] = splice_dist
    filter_flags["splice_dist_min_pass"] = splice_dist_min_pass
    filter_flags["set_MuTect_Rescue"] = set_MuTect_Rescue

    #
    # ~~~~~~~~ KEEP THESE MUTATIONS ~~~~~~ #
    #
    # Store all fillout rows
    if Mutation_Status_None:
        fillout_keep = True
        reject_row = False
        return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags)
    #
    # ~~~~~~~~~~~~~~ #
    #

    # Skip any that failed false-positive filters, except common_variant and Skip all events reported uniquely by Pindel
    if not pass_FILTER_or_is_common_variant_or_is_common_variant_and_is_not_Pindel:
        reject_reason = 'Skip any that failed false-positive filters, except common_variant and Skip all events reported uniquely by Pindel'
        reject_flag = "pass_FILTER_or_is_common_variant_or_is_common_variant_and_is_not_Pindel"

    # Skip any that failed false-positive filters, except common_variant and Skip all events reported uniquely by Pindel
    if pass_FILTER_or_is_common_variant_or_is_common_variant_and_is_not_Pindel:
        # Skip MuTect-Rescue events for all but IMPACT/HemePACT projects
        if set_MuTect_Rescue_and_not_is_impact:
            reject_row = True
            reject_reason = 'Skip MuTect-Rescue events for all but IMPACT/HemePACT projects'
            reject_flag = "set_MuTect_Rescue_and_not_is_impact"
            return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags)

        # Skip splice region variants in non-coding genes, or those that are >3bp into introns
        if splice_region_variant_with_Consequence:
            if non_coding_with_Consequence:
                reject_row = True
                reject_reason = 'Skip splice region variants in non-coding genes'
                reject_flag = "non_coding_with_Consequence"
                return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags)

            # Parse the complex HGVSc format to determine the distance from the splice junction
            if HGVSc_splice_match_is_not_None:
                if splice_dist_min_pass:
                    reject_row = True
                    reject_reason = 'Skip splice region variants that are >3bp into introns'
                    reject_flag = "splice_dist_min_pass"
                    return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags)

        if not pass_consequence_or_is_TERT:
            reject_reason = 'Skip all non-coding events except interesting ones like TERT promoter mutations'
            reject_flag = 'pass_consequence_or_is_TERT'

        # Skip all non-coding events except interesting ones like TERT promoter mutations
        if pass_consequence_or_is_TERT:
            # Skip reporting MT muts in IMPACT, and apply the DMP's depth/allele-count/VAF cutoffs as hard filters in IMPACT, and soft filters in non-IMPACT
            if is_impact_and_is_MT:
                reject_row = True
                reject_reason = 'Skip reporting MT muts in IMPACT'
                reject_flag = "is_impact_and_is_MT"
                return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags)

            if dmp_fail_and_is_impact:
                reject_row = True
                reject_reason = 'Apply the DMP depth/allele-count/VAF cutoffs as hard filters in IMPACT, and soft filters in non-IMPACT'
                reject_flag = "dmp_fail_and_is_impact"
                return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags)

            #
            # ~~~~~~~~ KEEP THESE MUTATIONS ~~~~~~ #
            #
            # The portal also skips silent muts, genes without Entrez IDs, and intronic events
            if silent_mut_no_entrez_intronic:
                portal_keep = True
                analysis_keep = True
                reject_row = False
                return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags)

            # tag this events in analysis maf as "skipped_by_portal" in column "Mutation_Status"
            else:
                row['Mutation_Status'] = "skipped_by_portal"
                analysis_keep = True
                reject_row = False
                return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags)
            #
            # ~~~~~~~~~~~~~~ #
            #

    return(row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags)

def filter_rows(
        row_list: List[Dict],
        is_impact: bool,
        keep_rejects: bool = False
        ) -> Tuple[ List[Dict], List[Dict], List[Dict], List[Dict] ]:
    """
    Filters the rows in the list
    """
    analysis_keep_list = []
    portal_keep_list = []
    fillout_keep_list = []
    rejected_list = []

    for row in row_list:
        new_row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags = filter_row(row, is_impact)
        if analysis_keep:
            analysis_keep_list.append(row)
        if portal_keep:
            portal_keep_list.append(row)
        if fillout_keep:
            fillout_keep_list.append(row)
        if keep_rejects:
            if reject_row:
                # make a copy of the row
                rejected_row = { k:v for k,v in row.items() }
                # add the reason to the row
                rejected_row['reject_reason'] = reject_reason
                rejected_row['reject_flag'] = reject_flag
                rejected_row['filter_flags'] = json.dumps(filter_flags)
                rejected_list.append(rejected_row)

    return(analysis_keep_list, portal_keep_list, fillout_keep_list, rejected_list)


def main(
    input_file: str,
    version_string: str,
    analyst_file: str,
    portal_file: str,
    is_impact: bool = True,
    rejected_file: str = 'rejected.muts.maf',
    keep_rejects: bool = False) -> None:
    """
    Main control function for the module when called as a script. Filters the input .maf file into an "analyst file" and a "portal file", meant to be used for downstream data analysis and for import to cBioPortal, respectively.

    Parameters
    ----------
    input_file: str
        the input .maf file to be filtered
    version_string: str
        a verstion label to be used in the output comment
    analyst_file: str
        the name of the analysis output file
    portal_file: str
        the name of the cBioPortal output file
    is_impact: bool
        wether the sample is IMPACT or not; adjusts filter criteria
    rejected_file: str
        the name of the file to save rejected variants to
    keep_rejects: bool
        wether or not to save rejected variants to the rejected_file
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
        # keep only a subset of fieldnames in the reject file output;
        reject_fieldnames_keep = [
        # keep every "row" field that is explicitly referenced in the filter_row function...
        'Amino_Acid_Change',
        'HGVSp_Short',
        'Variant_Type',
        't_depth',
        't_alt_count',
        'fillout_t_depth',
        'fillout_t_alt',
        'FILTER',
        'HGVSc',
        'set',
        'Mutation_Status',
        'Consequence',
        'Hugo_Symbol',
        'Start_Position',
        'Chromosome',
        'hotspot_whitelist',
        'Entrez_Gene_Id',
        # extra fields for easy variant idenfitication
        "End_Position",
        "Variant_Classification",
        "Reference_Allele",
        "Tumor_Seq_Allele1",
        "Tumor_Seq_Allele2",
        "Tumor_Sample_Barcode",
        "Matched_Norm_Sample_Barcode",
        "Match_Norm_Seq_Allele1",
        "Match_Norm_Seq_Allele2",
        "HGVSp",
        "Transcript_ID"
        "Exon_Number",
        "t_ref_count",
        "n_depth",
        "n_ref_count",
        "n_alt_count"
        # "all_effects" # this one is too long
        ]
        reject_fieldnames_remove = []
        reject_fieldnames = [ f for f in fieldnames if f in reject_fieldnames_keep ]
        reject_fieldnames.append('reject_reason')
        reject_fieldnames.append('reject_flag')
        reject_fieldnames.append('filter_flags')

        with open(rejected_file, "w") as fout:
            writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = reject_fieldnames, extrasaction = 'ignore', lineterminator='\n')
            writer.writeheader()
            for row in rejected_list:
                writer.writerow(row)

def parse():
    """
    Parse the CLI args

    maf_filter.py Proj_08390_G.muts.maf 2.x True analyst_file3.tsv portal_file3.tsv
    """
    parser = argparse.ArgumentParser(description = 'Script for filtering mutations in a .maf file')
    parser.add_argument('input_file', help='Input maf file')
    parser.add_argument('--version-string', dest = 'version_string', required = True, help='Version string label for output file comments')
    parser.add_argument('--analyst-file', dest = 'analyst_file', required = True, help='Filename for filtered analysis file output')
    parser.add_argument('--portal-file', dest = 'portal_file', required = True, help='Filename for filtered cBioPortal file output')
    parser.add_argument('--rejected-file', dest = 'rejected_file', default = 'rejected.muts.maf', help='Filename for rejected variants output')
    parser.add_argument('--keep-rejects', dest = 'keep_rejects', action="store_true", help='Whether to save rejected variants to the rejected file')
    parser.add_argument('--is-impact', action="store_true", help='Whether the sample is an IMPACT sample or not')
    args = parser.parse_args()

    main(**vars(args))

if __name__ == '__main__':
    parse()
