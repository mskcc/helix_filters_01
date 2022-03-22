"""
examples of mutations for use with test cases for

maf_filter.py
cBioPortal_utils.py

"""
# some demo maf rows to use in tests
bad_row_PNISR = { # bad row
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

good_row_FGF3 = { # good row
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

bad_row_set_Pindel = { # good row but set = Pindel
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

bad_row_set_MutectRescue = { # good row but set = MuTect-Rescue, is_impact = False
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

bad_row_cqs_splice = { # good row but Consequence = splice_region_variant & non_coding_
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

bad_row_csq_splice2 = { # good row but Consequence = splice_region_variant &  "HGVSc" : "c.542-4G>T",
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

bad_row_MT = { # good row but Chromosome = MT
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

bad_row_AF = { # good row but tumor_vaf < 0.05 (t_alt_count / t_depth ; fillout_t_alt / fillout_t_depth) and hotspot_whitelist = False
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
