#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
doc: '
Workflow for running the facets suite workflow on a single tumor normal pair
'

inputs:
  tumor_bam: File
  normal_bam: File
  pair_maf: File
  pair_id: string
  snps_vcf: File

steps:
  snp_pileup:
    run: snp-pileup-wrapper.cwl
    in:
      snps_vcf: snps_vcf
      normal_bam: normal_bam
      tumor_bam: tumor_bam
      output_prefix: pair_id
    out:
      [ output_file ]

  run_facets:
    run: run-facets-wrapper.cwl
    in:
      snp_pileup: snp_pileup/output_file
      sample_id: pair_id
    out: [ purity_seg, hisens_seg, qc_txt, gene_level_txt, arm_level_txt, output_txt, purity_rds, hisens_rds ]

  annotate_maf:
    run: annotate-maf-wrapper.cwl
    in:
      pair_id: pair_id
      maf_file: pair_maf
      facets_rds: run_facets/hisens_rds
      output_filename:
        valueFrom: $(inputs.pair_id)_hisens.ccf.maf
    out:
      [ output_file ]

outputs:
  pair_id:
    type: string
    outputSource: pair_id
  snp_pileup:
    type: File
    outputSource: snp_pileup/output_file
  purity_seg:
    type: File
    outputSource: run_facets/purity_seg
  hisens_seg:
    type: File
    outputSource: run_facets/hisens_seg
  qc_txt:
    type: File
    outputSource: run_facets/qc_txt
  gene_level_txt:
    type: File
    outputSource: run_facets/gene_level_txt
  arm_level_txt:
    type: File
    outputSource: run_facets/arm_level_txt
  facets_txt:
    type: File
    outputSource: run_facets/output_txt
  purity_rds:
    type: File
    outputSource: run_facets/purity_rds
  hisens_rds:
    type: File
    outputSource: run_facets/hisens_rds
  annotated_maf:
    type: File
    outputSource: annotate_maf/output_file
