#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the maf_filter.py script
"""
import sys
import os
import unittest
import csv
from tempfile import TemporaryDirectory

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command, load_mutations
    from .settings import DATA_SETS, BIN_DIR

if __name__ == "__main__":
    from tools import run_command, load_mutations
    from settings import DATA_SETS, BIN_DIR

# need to import the module from the other dir
THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from bin.cBioPortal_utils import parse_header_comments
from bin import maf_filter
sys.path.pop(0)


maf_filter_script = os.path.join(BIN_DIR, 'maf_filter.py')

class TestMafFilterScript(unittest.TestCase):
    def test_maf_filter_script1(self):
        """
        Test run of the maf_filter.py script on a sample pair .maf file and validate the results contain the expected variants
        """
        # sample input files to use
        input_maf_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'Sample1.Sample2.muts.maf')
        expected_analyst_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'analyst_file.txt') # 24
        expected_portal_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'portal_file.txt') # 19

        # NOTE: skip this it takes too long
        # input fixture has the correct number of lines
        # with open(input_maf_file) as fin:
        #     input_maf_lines = len(fin.readlines())
        # self.assertEqual(input_maf_lines, 12518)

        # run the maf_filter.py script in a temporary directory
        with TemporaryDirectory() as tmpdir:
            # files to output
            analyst_file = os.path.join(tmpdir, "analyst_file.txt")
            portal_file = os.path.join(tmpdir, "portal_file.txt")
            rejected_file = os.path.join(tmpdir, "rejected.muts.maf")

            # command line arguments to run script
            command = [ maf_filter_script, input_maf_file, '--version-string', "2.x", "--is-impact", '--analyst-file', analyst_file, '--portal-file', portal_file, '--keep-rejects', '--rejected-file', rejected_file ]

            # run the script in a subprocess
            returncode, proc_stdout, proc_stderr = run_command(command)

            # check that it ran successfully
            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            # check the number of lines output
            with open(analyst_file) as fin:
                num_lines_analyst_file = len(fin.readlines())

            with open(portal_file) as fin:
                num_lines_portal_file = len(fin.readlines())

            with open(rejected_file) as fin:
                num_lines_rejected_file = len(fin.readlines())

            self.assertEqual(num_lines_analyst_file, 27)
            self.assertEqual(num_lines_portal_file, 22)
            self.assertEqual(num_lines_rejected_file, 12493)

            # check the comments written to the output files
            comments, start_line = parse_header_comments(portal_file)
            expected_comments = [
                '#version 2.4',
                '#ngs-filters/applyFilter.sh VERSION=v1.2.1 FILTER=filter_blacklist_regions.R',
                '#ngs-filters/applyFilter.sh VERSION=v1.2.1 FILTER=filter_normal_panel.R',
                '# Versions: 2.x'
            ]
            self.assertEqual(comments, expected_comments)

            # check the number of variants written to the file (no comments)
            with open(portal_file) as fin:
                while start_line > 0:
                    next(fin)
                    start_line -= 1
                reader = csv.DictReader(fin, delimiter = '\t') # header_line = next(fin)
                portal_lines = [ row for row in reader ]

            self.assertEqual(len(portal_lines), 17)

            # get a subset of the lines' data for testing; too many columns to save here
            portal_mutations = []
            for row in portal_lines:
                t = ( row["Chromosome"], row["Start_Position"], row["End_Position"] )
                portal_mutations.append(t)

            # block of text copied from portal file; Chromosome	Start_Position	End_Position
            expected_contents = """8	56912099	56912099
X	123220555	123220555
11	69625447	69625447
17	78938112	78938113
12	102796343	102796343
6	117687313	117687313
8	141566089	141566089
10	70406514	70406514
X	76938716	76938716
6	117622265	117622265
5	1295250	1295250
5	176721774	176721774
12	57864555	57864555
19	11018780	11018782
5	176522632	176522632
8	69136857	69136857
7	2953083	2953083"""
            expected_contents = expected_contents.split('\n')
            expected_rows = []
            for item in expected_contents:
                Chromosome, Start_Position, End_Position = item.split('\t')
                t = ( Chromosome, Start_Position, End_Position )
                expected_rows.append(t)

            # make sure all the expected values are present
            self.assertEqual(set(portal_mutations), set(expected_rows))

            # check the comments and variants output by the analysis file as well
            comments, start_line = parse_header_comments(analyst_file)
            expected_comments = [
            '#version 2.4',
            '#ngs-filters/applyFilter.sh VERSION=v1.2.1 FILTER=filter_blacklist_regions.R',
            '#ngs-filters/applyFilter.sh VERSION=v1.2.1 FILTER=filter_normal_panel.R',
            '# Versions: 2.x'
            ]
            self.assertEqual(comments, expected_comments)
            with open(analyst_file) as fin:
                while start_line > 0:
                    next(fin)
                    start_line -= 1
                reader = csv.DictReader(fin, delimiter = '\t') # header_line = next(fin)
                analysis_lines = [ row for row in reader ]

            self.assertEqual(len(analysis_lines), 22)

            analysis_mutations = []
            for row in analysis_lines:
                t = ( row["Chromosome"], row["Start_Position"], row["End_Position"] )
                analysis_mutations.append(t)

            # block of text copied from analyst file; Chromosome	Start_Position	End_Position
            expected_contents = """11	69625447	69625447
8	69136857	69136857
8	141566089	141566089
X	76938716	76938716
12	49419992	49419992
X	123220555	123220555
5	176721774	176721774
19	11018780	11018782
5	176522632	176522632
8	56912099	56912099
17	78938112	78938113
12	57864555	57864555
6	117687313	117687313
10	70406514	70406514
3	142281434	142281434
5	1295250	1295250
6	117609901	117609901
12	102796343	102796343
6	117622265	117622265
12	121438953	121438953
7	2953083	2953083
2	212989483	212989483"""
            expected_contents = expected_contents.split('\n')
            expected_rows = []
            for item in expected_contents:
                Chromosome, Start_Position, End_Position = item.split('\t')
                t = ( Chromosome, Start_Position, End_Position )
                expected_rows.append(t)

            # make sure all the expected values are present
            self.assertEqual(set(analysis_mutations), set(expected_rows))

    def test_filter_maf_file_impact_false(self):
        """
        Test the maf_filter.py results with IMPACT flag not set
        """
        input_maf_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], 'Sample1', 'Sample1.Sample2.muts.maf')

        with TemporaryDirectory() as tmpdir:
            # files to output
            analyst_file = os.path.join(tmpdir, "analyst_file.txt")
            portal_file = os.path.join(tmpdir, "portal_file.txt")
            rejected_file = os.path.join(tmpdir, "rejected.muts.maf")

            # command line arguments to run script
            command = [ maf_filter_script, input_maf_file, '--version-string', "2.x", '--analyst-file', analyst_file, '--portal-file', portal_file, '--keep-rejects', '--rejected-file', rejected_file ]

            # run the script in a subprocess
            returncode, proc_stdout, proc_stderr = run_command(command)

            # check that it ran successfully
            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            # check the number of lines output
            with open(analyst_file) as fin:
                num_lines_analyst_file = len(fin.readlines())

            with open(portal_file) as fin:
                num_lines_portal_file = len(fin.readlines())

            with open(rejected_file) as fin:
                num_lines_rejected_file = len(fin.readlines())

            self.assertEqual(num_lines_analyst_file, 23)
            self.assertEqual(num_lines_portal_file, 19)
            self.assertEqual(num_lines_rejected_file, 12497)

    def test_filter_test_large_maf_file(self):
        """
        Test that a giant maf file with tons of variants gets filtered as expected
        """
        input_maf_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], "Proj_08390_G", "Proj_08390_G.muts.maf")

        # NOTE: skip this it takes too long
        # make sure input file has expected number of lines
        # comments, mutations = load_mutations(input_maf_file, delete_cols = True) # try to reduce memory usage by deleting columns
        # self.assertEqual(len(mutations), 710324)

        # run the filter script
        with TemporaryDirectory() as tmpdir:
            # output files
            analyst_file = os.path.join(tmpdir, "analyst_file.txt")
            portal_file = os.path.join(tmpdir, "portal_file.txt")
            rejected_file = os.path.join(tmpdir, "rejected.muts.maf")

            # run the command
            command = [ maf_filter_script, input_maf_file, '--version-string', "2.x", "--is-impact", '--analyst-file', analyst_file, '--portal-file', portal_file, '--keep-rejects', '--rejected-file', rejected_file ]
            returncode, proc_stdout, proc_stderr = run_command(command)

            # check that it ran successfully
            if returncode != 0:
                print(proc_stderr)
            self.assertEqual(returncode, 0)

            # check number of output lines
            with open(analyst_file) as fin:
                num_lines_analyst_file = len(fin.readlines())

            with open(portal_file) as fin:
                num_lines_portal_file = len(fin.readlines())

            with open(rejected_file) as fin:
                num_lines_rejected_file = len(fin.readlines())

            self.assertEqual(num_lines_analyst_file, 1664)
            self.assertEqual(num_lines_portal_file, 1141)
            self.assertEqual(num_lines_rejected_file, 708663)

            # validate output mutation file contents
            comments, mutations = load_mutations(analyst_file)
            expected_comments, expected_mutations = load_mutations(os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], "Proj_08390_G", "analyst_file.txt"))

            for mutation in expected_mutations:
                self.assertTrue(mutation in mutations)

            self.assertEqual(len(mutations), len(expected_mutations))

            comments, mutations = load_mutations(portal_file)
            expected_comments, expected_mutations = load_mutations(os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], "Proj_08390_G", "portal_file.txt"))

            for mutation in expected_mutations:
                self.assertTrue(mutation in mutations)

            self.assertEqual(len(mutations), len(expected_mutations))

            comments, mutations = load_mutations(rejected_file)
            self.assertEqual(len(mutations), 708662)

    def test_filter_test_large_maf_file_impact_false(self):
        """
        Filter the large maf file without IMPACT flag used and check the number of mutations output
        """
        input_maf_file = os.path.join(DATA_SETS['Proj_08390_G']['MAF_FILTER_DIR'], "Proj_08390_G", "Proj_08390_G.muts.maf")

        with TemporaryDirectory() as tmpdir:
            # output files
            analyst_file = os.path.join(tmpdir, "analyst_file.txt")
            portal_file = os.path.join(tmpdir, "portal_file.txt")
            rejected_file = os.path.join(tmpdir, "rejected.muts.maf")

            # run the command
            command = [ maf_filter_script, input_maf_file, '--version-string', "2.x", '--analyst-file', analyst_file, '--portal-file', portal_file, '--keep-rejects', '--rejected-file', rejected_file ]
            returncode, proc_stdout, proc_stderr = run_command(command)

            # check that it ran successfully
            if returncode != 0:
                print(proc_stderr)
            self.assertEqual(returncode, 0)

            # check number of output lines and mutations
            with open(analyst_file) as fin:
                num_lines_analyst_file = len(fin.readlines())

            with open(portal_file) as fin:
                num_lines_portal_file = len(fin.readlines())

            with open(rejected_file) as fin:
                num_lines_rejected_file = len(fin.readlines())

            self.assertEqual(num_lines_analyst_file, 1996)
            self.assertEqual(num_lines_portal_file, 1410)
            self.assertEqual(num_lines_rejected_file, 708331)

            comments, mutations = load_mutations(analyst_file)
            self.assertEqual(len(mutations), 1994)

            comments, mutations = load_mutations(portal_file)
            self.assertEqual(len(mutations), 1408)

            comments, mutations = load_mutations(rejected_file)
            self.assertEqual(len(mutations), 708330)

class TestMafFilter2Script(unittest.TestCase):
    def test_filter_single_bad_rows1(self):
        """
        Test that single bad rows gets filtered as expected
        This set of bad rows should hit at least one failure condition in each of the main criteria sets configured in the maf_filter
        filter code if/else series
        """
        row = { # bad row
        "Hugo_Symbol" : "PNISR",
        "Entrez_Gene_Id" : "25957",
        "Chromosome" : "6",
        "Start_Position" : "99865784",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "A",
        "Mutation_Status" : "",
        "HGVSc" : "c.-111-1480G>T",
        "HGVSp_Short" : "",
        "t_depth" : "6",
        "t_alt_count" : "3",
        "Consequence" : "intron_variant",
        "FILTER" : "q22.5;hstdp;hsndp;hstad",
        "ExAC_FILTER" : "",
        "set" : "VarDict",
        "fillout_t_depth" : "8",
        "fillout_t_alt" : "5",
        "hotspot_whitelist" : "FALSE",
        }
        new_row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags = maf_filter.filter_row(row, is_impact = True)

        self.assertDictEqual(new_row, row)
        self.assertEqual(analysis_keep, False)
        self.assertEqual(portal_keep, False)
        self.assertEqual(fillout_keep, False)
        self.assertEqual(reject_row, True)
        self.assertEqual(reject_reason, 'Skip any that failed false-positive filters, except common_variant and Skip all events reported uniquely by Pindel')
        self.assertEqual(reject_flag, 'pass_FILTER_or_is_common_variant_or_is_common_variant_and_is_not_Pindel')

        # good row but set = Pindel
        row = {
        "Hugo_Symbol" : "FGF3",
        "Entrez_Gene_Id" : "2248",
        "Chromosome" : "11",
        "Start_Position" : "69625447",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "T",
        "Mutation_Status" : "",
        "HGVSc" : "c.346G>A",
        "HGVSp_Short" : "p.E116K",
        "t_depth" : "109",
        "t_alt_count" : "16",
        "Consequence" : "missense_variant",
        "FILTER" : "PASS",
        "ExAC_FILTER" : "PASS",
        "set" : "Pindel",
        "fillout_t_depth" : "122",
        "fillout_t_alt" : "28",
        "hotspot_whitelist" : "FALSE"
        }
        new_row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags = maf_filter.filter_row(row, is_impact = True)
        self.assertDictEqual(new_row, row)
        self.assertEqual(analysis_keep, False)
        self.assertEqual(portal_keep, False)
        self.assertEqual(fillout_keep, False)
        self.assertEqual(reject_row, True)
        self.assertEqual(reject_reason, 'Skip any that failed false-positive filters, except common_variant and Skip all events reported uniquely by Pindel')
        self.assertEqual(reject_flag, 'pass_FILTER_or_is_common_variant_or_is_common_variant_and_is_not_Pindel')

        # good row but set = MuTect-Rescue, is_impact = False
        row = {
        "Hugo_Symbol" : "FGF3",
        "Entrez_Gene_Id" : "2248",
        "Chromosome" : "11",
        "Start_Position" : "69625447",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "T",
        "Mutation_Status" : "",
        "HGVSc" : "c.346G>A",
        "HGVSp_Short" : "p.E116K",
        "t_depth" : "109",
        "t_alt_count" : "16",
        "Consequence" : "missense_variant",
        "FILTER" : "PASS",
        "ExAC_FILTER" : "PASS",
        "set" : "MuTect-Rescue",
        "fillout_t_depth" : "122",
        "fillout_t_alt" : "28",
        "hotspot_whitelist" : "FALSE"
        }
        new_row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags = maf_filter.filter_row(row, is_impact = False)
        self.assertDictEqual(new_row, row)
        self.assertEqual(analysis_keep, False)
        self.assertEqual(portal_keep, False)
        self.assertEqual(fillout_keep, False)
        self.assertEqual(reject_row, True)
        self.assertEqual(reject_reason, 'Skip MuTect-Rescue events for all but IMPACT/HemePACT projects')
        self.assertEqual(reject_flag, 'set_MuTect_Rescue_and_not_is_impact')

        # good row but Consequence = splice_region_variant & non_coding_
        row = {
        "Hugo_Symbol" : "FGF3",
        "Entrez_Gene_Id" : "2248",
        "Chromosome" : "11",
        "Start_Position" : "69625447",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "T",
        "Mutation_Status" : "",
        "HGVSc" : "c.346G>A",
        "HGVSp_Short" : "p.E116K",
        "t_depth" : "109",
        "t_alt_count" : "16",
        "Consequence" : "splice_region_variant,non_coding_",
        "FILTER" : "PASS",
        "ExAC_FILTER" : "PASS",
        "set" : "MuTect",
        "fillout_t_depth" : "122",
        "fillout_t_alt" : "28",
        "hotspot_whitelist" : "FALSE"
        }
        new_row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags = maf_filter.filter_row(row, is_impact = True)
        self.assertDictEqual(new_row, row)
        self.assertEqual(analysis_keep, False)
        self.assertEqual(portal_keep, False)
        self.assertEqual(fillout_keep, False)
        self.assertEqual(reject_row, True)
        self.assertEqual(reject_reason, 'Skip splice region variants in non-coding genes')
        self.assertEqual(reject_flag, 'non_coding_with_Consequence')

        # good row but Consequence = splice_region_variant &  "HGVSc" : "c.542-4G>T",
        row = {
        "Hugo_Symbol" : "FGF3",
        "Entrez_Gene_Id" : "2248",
        "Chromosome" : "11",
        "Start_Position" : "69625447",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "T",
        "Mutation_Status" : "",
        "HGVSc" : "c.542-4G>T",
        "HGVSp_Short" : "p.E116K",
        "t_depth" : "109",
        "t_alt_count" : "16",
        "Consequence" : "splice_region_variant",
        "FILTER" : "PASS",
        "ExAC_FILTER" : "PASS",
        "set" : "MuTect",
        "fillout_t_depth" : "122",
        "fillout_t_alt" : "28",
        "hotspot_whitelist" : "FALSE"
        }
        new_row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags = maf_filter.filter_row(row, is_impact = True)
        self.assertDictEqual(new_row, row)
        self.assertEqual(analysis_keep, False)
        self.assertEqual(portal_keep, False)
        self.assertEqual(fillout_keep, False)
        self.assertEqual(reject_row, True)
        self.assertEqual(reject_reason, 'Skip splice region variants that are >3bp into introns')
        self.assertEqual(reject_flag, 'splice_dist_min_pass')

        # good row but Consequence = something bad
        # some bad consequence examples;
        bad_csqs = [
        '3_prime_UTR_variant',
        '5_prime_UTR_variant',
        'downstream_gene_variant',
        'intron_variant',
        'intron_variant,non_coding_transcript_variant',
        'non_coding_transcript_exon_variant,non_coding_transcript_variant',
        'upstream_gene_variant'
        ]
        for bad_csq in bad_csqs:
            row = {
            "Hugo_Symbol" : "FGF3",
            "Entrez_Gene_Id" : "2248",
            "Chromosome" : "11",
            "Start_Position" : "69625447",
            "Variant_Type" : "SNP",
            "Reference_Allele" : "C",
            "Tumor_Seq_Allele2" : "T",
            "Mutation_Status" : "",
            "HGVSc" : "c.346G>A",
            "HGVSp_Short" : "p.E116K",
            "t_depth" : "109",
            "t_alt_count" : "16",
            "Consequence" : bad_csq,
            "FILTER" : "PASS",
            "ExAC_FILTER" : "PASS",
            "set" : "MuTect",
            "fillout_t_depth" : "122",
            "fillout_t_alt" : "28",
            "hotspot_whitelist" : "FALSE"
            }
            new_row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags = maf_filter.filter_row(row, is_impact = True)
            self.assertDictEqual(new_row, row)
            self.assertEqual(analysis_keep, False)
            self.assertEqual(portal_keep, False)
            self.assertEqual(fillout_keep, False)
            self.assertEqual(reject_row, True)
            self.assertEqual(reject_reason, 'Skip all non-coding events except interesting ones like TERT promoter mutations')
            self.assertEqual(reject_flag, 'pass_consequence_or_is_TERT')

        # good row but Chromosome = MT
        row = {
        "Hugo_Symbol" : "FGF3",
        "Entrez_Gene_Id" : "2248",
        "Chromosome" : "MT",
        "Start_Position" : "69625447",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "T",
        "Mutation_Status" : "",
        "HGVSc" : "c.542-4G>T",
        "HGVSp_Short" : "p.E116K",
        "t_depth" : "109",
        "t_alt_count" : "16",
        "Consequence" : "missense_variant",
        "FILTER" : "PASS",
        "ExAC_FILTER" : "PASS",
        "set" : "MuTect",
        "fillout_t_depth" : "122",
        "fillout_t_alt" : "28",
        "hotspot_whitelist" : "FALSE"
        }
        new_row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags = maf_filter.filter_row(row, is_impact = True)
        self.assertDictEqual(new_row, row)
        self.assertEqual(analysis_keep, False)
        self.assertEqual(portal_keep, False)
        self.assertEqual(fillout_keep, False)
        self.assertEqual(reject_row, True)
        self.assertEqual(reject_reason, 'Skip reporting MT muts in IMPACT')
        self.assertEqual(reject_flag, 'is_impact_and_is_MT')

        # some example bad mutations:
        # {'t_depth': 919, 'fail_DMP_t_depth': False, 't_alt_count': 37, 'fail_DMP_t_alt_count': False, 'tumor_vaf': 0.04026115342763874, 'fail_DMP_tumor_vaf': False, 'hotspot_whitelist': 'FALSE', 'fail_DMP_whitelist_filter': True}
        # {'t_depth': 41, 'fail_DMP_t_depth': False, 't_alt_count': 5, 'fail_DMP_t_alt_count': True, 'tumor_vaf': 0.12195121951219512, 'fail_DMP_tumor_vaf': False, 'hotspot_whitelist': 'FALSE', 'fail_DMP_whitelist_filter': True}
        # {'t_depth': 145, 'fail_DMP_t_depth': False, 't_alt_count': 8, 'fail_DMP_t_alt_count': False, 'tumor_vaf': 0.05517241379310345, 'fail_DMP_tumor_vaf': False, 'hotspot_whitelist': 'FALSE', 'fail_DMP_whitelist_filter': True}


        # good row but tumor_vaf < 0.05 (t_alt_count / t_depth ; fillout_t_alt / fillout_t_depth) and hotspot_whitelist = False
        row = {
        "Hugo_Symbol" : "FGF3",
        "Entrez_Gene_Id" : "2248",
        "Chromosome" : "11",
        "Start_Position" : "69625447",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "T",
        "Mutation_Status" : "",
        "HGVSc" : "c.346G>A",
        "HGVSp_Short" : "p.E116K",
        "t_depth" : "0", # dummy values that wont get used
        "t_alt_count" : "0", # dummy values that wont get used
        "Consequence" : "frameshift_variant",
        "FILTER" : "PASS",
        "ExAC_FILTER" : "PASS",
        "set" : "MuTect",
        "fillout_t_depth" : "919",
        "fillout_t_alt" : "37",
        "hotspot_whitelist" : "FALSE"
        }
        new_row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags = maf_filter.filter_row(row, is_impact = True)
        self.assertDictEqual(new_row, row)
        self.assertEqual(analysis_keep, False)
        self.assertEqual(portal_keep, False)
        self.assertEqual(fillout_keep, False)
        self.assertEqual(reject_row, True)
        self.assertEqual(reject_reason, 'Apply the DMP depth/allele-count/VAF cutoffs as hard filters in IMPACT, and soft filters in non-IMPACT')
        self.assertEqual(reject_flag, 'dmp_fail_and_is_impact')


    def test_filter_single_good_row1(self):
        """
        Test that a single good row gets filtered as expected
        """
        row = { # good row
        "Hugo_Symbol" : "FGF3",
        "Entrez_Gene_Id" : "2248",
        "Chromosome" : "11",
        "Start_Position" : "69625447",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "T",
        "Mutation_Status" : "",
        "HGVSc" : "c.346G>A",
        "HGVSp_Short" : "p.E116K",
        "t_depth" : "109",
        "t_alt_count" : "16",
        "Consequence" : "missense_variant",
        "FILTER" : "PASS",
        "ExAC_FILTER" : "PASS",
        "set" : "MuTect",
        "fillout_t_depth" : "122",
        "fillout_t_alt" : "28",
        "hotspot_whitelist" : "FALSE"
        }
        new_row, analysis_keep, portal_keep, fillout_keep, reject_row, reject_reason, reject_flag, filter_flags = maf_filter.filter_row(row, is_impact = True)

        self.assertDictEqual(new_row, row)
        self.assertEqual(analysis_keep, True)
        self.assertEqual(portal_keep, True)
        self.assertEqual(fillout_keep, False)
        self.assertEqual(reject_row, False)
        self.assertEqual(reject_reason, None)
        self.assertEqual(reject_flag, None)

    def test_maf_filter2_filter_rows(self):
        """
        Test that rows get filtered from the maf_filter module as expected
        """
        row1 = { # bad row
        "Hugo_Symbol" : "PNISR",
        "Entrez_Gene_Id" : "25957",
        "Chromosome" : "6",
        "Start_Position" : "99865784",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "A",
        "Mutation_Status" : "",
        "HGVSc" : "c.-111-1480G>T",
        "HGVSp_Short" : "",
        "t_depth" : "6",
        "t_alt_count" : "3",
        "Consequence" : "intron_variant",
        "FILTER" : "q22.5;hstdp;hsndp;hstad",
        "ExAC_FILTER" : "",
        "set" : "VarDict",
        "fillout_t_depth" : "8",
        "fillout_t_alt" : "5",
        "hotspot_whitelist" : "FALSE",
        }
        row2 = { # good row
        "Hugo_Symbol" : "FGF3",
        "Entrez_Gene_Id" : "2248",
        "Chromosome" : "11",
        "Start_Position" : "69625447",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "T",
        "Mutation_Status" : "",
        "HGVSc" : "c.346G>A",
        "HGVSp_Short" : "p.E116K",
        "t_depth" : "109",
        "t_alt_count" : "16",
        "Consequence" : "missense_variant",
        "FILTER" : "PASS",
        "ExAC_FILTER" : "PASS",
        "set" : "MuTect",
        "fillout_t_depth" : "122",
        "fillout_t_alt" : "28",
        "hotspot_whitelist" : "FALSE"
        }

        row_list = [row1, row2]

        analysis_keep, portal_keep, fillout_keep, rejected_list = maf_filter.filter_rows(row_list, is_impact = True)

        self.assertEqual(analysis_keep, [row2])
        self.assertEqual(portal_keep, [row2])
        self.assertEqual(fillout_keep, [])

    def test_maf_filter2_script(self):
        """
        Test that a maf file with comment line, one good variant, and one bad variant, produce the expected output
        """
        comments = [
        '# some comment goes here\n'
        ]
        row1 = { # bad row
        "Hugo_Symbol" : "PNISR",
        "Entrez_Gene_Id" : "25957",
        "Chromosome" : "6",
        "Start_Position" : "99865784",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "A",
        "Mutation_Status" : "",
        "HGVSc" : "c.-111-1480G>T",
        "HGVSp_Short" : "",
        "t_depth" : "6",
        "t_alt_count" : "3",
        "Consequence" : "intron_variant",
        "FILTER" : "q22.5;hstdp;hsndp;hstad",
        "ExAC_FILTER" : "",
        "set" : "VarDict",
        "fillout_t_depth" : "8",
        "fillout_t_alt" : "5",
        "hotspot_whitelist" : "FALSE",
        }
        row2 = { # good row
        "Hugo_Symbol" : "FGF3",
        "Entrez_Gene_Id" : "2248",
        "Chromosome" : "11",
        "Start_Position" : "69625447",
        "Variant_Type" : "SNP",
        "Reference_Allele" : "C",
        "Tumor_Seq_Allele2" : "T",
        "Mutation_Status" : "",
        "HGVSc" : "c.346G>A",
        "HGVSp_Short" : "p.E116K",
        "t_depth" : "109",
        "t_alt_count" : "16",
        "Consequence" : "missense_variant",
        "FILTER" : "PASS",
        "ExAC_FILTER" : "PASS",
        "set" : "MuTect",
        "fillout_t_depth" : "122",
        "fillout_t_alt" : "28",
        "hotspot_whitelist" : "FALSE"
        }

        row_list = [row1, row2]

        with TemporaryDirectory() as tmpdir:
            input_maf_file = os.path.join(tmpdir, "input.txt")
            analyst_file = os.path.join(tmpdir, "analyst_file.txt")
            portal_file = os.path.join(tmpdir, "portal_file.txt")
            rejected_file = os.path.join(tmpdir, "rejected.muts.maf")

            # write out the intput maf
            with open(input_maf_file, "w") as fout:
                fout.writelines(comments)
                writer = csv.DictWriter(fout, delimiter = '\t', fieldnames = row1.keys())
                writer.writeheader()
                for row in row_list:
                    writer.writerow(row)

            command = [ maf_filter_script, input_maf_file, '--version-string', "2.x", "--is-impact", '--analyst-file', analyst_file, '--portal-file', portal_file, '--keep-rejects', '--rejected-file', rejected_file ]

            returncode, proc_stdout, proc_stderr = run_command(command)

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            with open(analyst_file) as fin:
                analyst_lines = fin.readlines()
            expected_analyst_lines = [
            '# some comment goes here\n',
            '# Versions: 2.x\n',
            'Hugo_Symbol\tEntrez_Gene_Id\tChromosome\tStart_Position\tVariant_Type\tReference_Allele\tTumor_Seq_Allele2\tMutation_Status\tHGVSc\tHGVSp_Short\tt_depth\tt_alt_count\tConsequence\tFILTER\tExAC_FILTER\tset\tfillout_t_depth\tfillout_t_alt\thotspot_whitelist\n',
            'FGF3\t2248\t11\t69625447\tSNP\tC\tT\t\tc.346G>A\tp.E116K\t109\t16\tmissense_variant\tPASS\tPASS\tMuTect\t122\t28\tFALSE\n'
            ]

            with open(portal_file) as fin:
                portal_lines = fin.readlines()
            expected_portal_lines = [
            '# some comment goes here\n',
            '# Versions: 2.x\n',
            'Hugo_Symbol\tEntrez_Gene_Id\tChromosome\tStart_Position\tVariant_Type\tReference_Allele\tTumor_Seq_Allele2\tMutation_Status\tHGVSc\tAmino_Acid_Change\tt_depth\tt_alt_count\n',
            'FGF3\t2248\t11\t69625447\tSNP\tC\tT\t\tc.346G>A\tp.E116K\t109\t16\n'
            ]

            self.assertEqual(len(analyst_lines), 4)
            self.assertEqual(len(portal_lines), 4)

            self.assertEqual(analyst_lines, expected_analyst_lines)
            self.assertEqual(portal_lines, expected_portal_lines)



if __name__ == "__main__":
    unittest.main()
