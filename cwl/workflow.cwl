#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

requirements:
  ScatterFeatureRequirement: {}

inputs:
  maf_files: File[]
  roslin_version_string:
    type: string
  is_impact:
    type: string
  analyst_file:
    type: string
  portal_file:
    type: string
  hisens_cncfs: File[]
  portal_CNA_file: string
  analysis_gene_cna_file: string
  targets_list: File

steps:
  strip_maf:
    run: strip.cwl
    scatter: input_file
    in:
      input_file: maf_files
    out:
      [output_file]

  concat_maf:
    run: concat.cwl
    in:
      input_files: strip_maf/output_file
    out:
      [output_file]

  maf_filter:
    run: maf_filter.cwl
    in:
      maf_file: concat_maf/output_file
      roslin_version_string: roslin_version_string
      is_impact: is_impact
      analyst_file: analyst_file
      portal_file: portal_file
    out: [analyst_file, portal_file]

  copy_number:
    run: copy_number.cwl
    in:
      portal_CNA_file: portal_CNA_file
      targets_list: targets_list
      hisens_cncfs: hisens_cncfs
    out: [output_portal_CNA_file]

  copy_cna_file:
    run: cp.cwl
    in:
      input_file: copy_number/output_portal_CNA_file
      output_filename: analysis_gene_cna_file
    out:
      [output_file]

outputs:
  analyst_file:
    type: File
    outputSource: maf_filter/analyst_file
  portal_file:
    type: File
    outputSource: maf_filter/portal_file
  output_portal_CNA_file:
    type: File
    outputSource: copy_number/output_portal_CNA_file
  analysis_gene_cna_file:
    type: File
    outputSource: copy_cna_file/output_file
