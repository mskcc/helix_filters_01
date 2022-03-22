#!/usr/bin/env python3
"""
Script to update columns in the custom samples fillout maf file for use with cBioPortal

Need to fix these columsn from fillout.maf for cBioPortal
    40  t_depth
    41  t_ref_count
    42  t_alt_count

using new fillout columns;

   139  t_FL_AD
   145  t_FL_DP
   151  t_FL_RD

from the vcf;
##FORMAT=<ID=FL_DP,Number=1,Type=Integer,Description="Total depth">
##FORMAT=<ID=FL_RD,Number=1,Type=Integer,Description="Depth matching reference (REF) allele">
##FORMAT=<ID=FL_AD,Number=1,Type=Integer,Description="Depth matching alternate (ALT) allele">
##FORMAT=<ID=FL_VF,Number=1,Type=Float,Description="Variant frequence (AD/DP)">
##FORMAT=<ID=FL_DPP,Number=1,Type=Integer,Description="Depth on postitive strand">
##FORMAT=<ID=FL_DPN,Number=1,Type=Integer,Description="Depth on negative strand">
##FORMAT=<ID=FL_RDP,Number=1,Type=Integer,Description="Reference depth on postitive strand">
##FORMAT=<ID=FL_RDN,Number=1,Type=Integer,Description="Reference depth on negative strand">
##FORMAT=<ID=FL_ADP,Number=1,Type=Integer,Description="Alternate depth on postitive strand">
##FORMAT=<ID=FL_ADN,Number=1,Type=Integer,Description="Alternate depth on negative strand">
##FORMAT=<ID=DPF,Number=1,Type=Integer,Description="Total fragment depth">
##FORMAT=<ID=RDF,Number=1,Type=Float,Description="Fragment depth matching reference (REF) allele">
##FORMAT=<ID=ADF,Number=1,Type=Float,Description="Fragment depth matching alternate (ALT) allele">

##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=AD,Number=R,Type=Integer,Description="Allelic Depths of REF and ALT(s) in the order listed">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
##INFO=<ID=AC,Number=A,Type=Integer,Description="Allele count in genotypes">
##INFO=<ID=AN,Number=1,Type=Integer,Description="Total number of alleles in called genotypes">


need to make new columns in the maf output
move the original t_depth, t_ref_count, t_alt_count values to new column labeled 't_depth_sample', etc..
update the existing values for ^^^ in order to back-fill empty values for fillout'd variants with values from
t_FL_DP, t_FL_RD, t_FL_AD

make sure NaN values are set to 0 as well

add a col is_fillout to label if a row was from fillout or not


-----
NOTE: MOVE MAF OUTPUT AND FORMATTER TO cBioPortal_utils.MafWriter !! DO NOT ADD MORE ONE-OFF MAF FORMATTING MODULES AND METHODS !!
-----


"""
import sys
import csv
args = sys.argv[1:]
input_file = args[0]
output_file = args[1]
# string in the input maf file that represents empty value
input_na_str = ''


with open(input_file) as fin, open(output_file, "w") as fout:
    # skip first line
    # TODO: handle comment lines better
    next(fin)

    reader = csv.DictReader(fin, delimiter = '\t')
    old_fieldnames = reader.fieldnames

    # append the new columns to the maf;
    new_fieldnames = [ f for f in old_fieldnames ]
    new_fieldnames.append('t_depth_sample') # t_depth
    new_fieldnames.append('t_ref_count_sample') # t_ref_count
    new_fieldnames.append('t_alt_count_sample') # t_alt_count
    new_fieldnames.append('is_fillout')

    writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = new_fieldnames, lineterminator='\n') # no carriage returns allowed
    writer.writeheader()

    for row in reader:
        # original values for the sample
        t_depth_sample = row['t_depth']
        t_ref_count_sample = row['t_ref_count']
        t_alt_count_sample = row['t_alt_count']

        # save the original values to new columns
        row['t_depth_sample'] = t_depth_sample
        row['t_ref_count_sample'] = t_ref_count_sample
        row['t_alt_count_sample'] = t_alt_count_sample

        # check if the variant was a fillout or not; SRC will not contain the Tumor_Sample_Barcode
        sample_id = row['Tumor_Sample_Barcode']
        samples = set(row['SRC'].split(','))
        row['is_fillout'] = not sample_id in samples

        # if any of the values was blank, replace with fillout values
        if any([t_depth_sample == input_na_str, t_ref_count_sample == input_na_str, t_alt_count_sample == input_na_str]):
            # get the values from fillout
            t_depth_fillout = row['t_FL_DP']
            t_ref_count_fillout = row['t_FL_RD']
            t_alt_count_fillout = row['t_FL_AD']

            # replace the values in the row with the fillout values
            row['t_depth'] = str(int(t_ref_count_fillout) + int(t_alt_count_fillout))
            row['t_ref_count'] = t_ref_count_fillout
            row['t_alt_count'] = t_alt_count_fillout

        writer.writerow(row)
