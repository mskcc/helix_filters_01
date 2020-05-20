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
    # need to remove the '#' comment lines from the maf so we can concat them cleanly later
    run: strip.cwl
    scatter: input_file
    in:
      input_file: maf_files
    out:
      [output_file]

  maf_filter:
    # filter each maf file
    run: maf_filter.cwl
    scatter: maf_file
    in:
      maf_file: strip_maf/output_file
      roslin_version_string: roslin_version_string
      is_impact: is_impact
      analyst_filename: analyst_file
      portal_filename: portal_file
    out: [analyst_file]

  concat_maf:
    # concat all the maf files into a single table
    run: concat.cwl
    in:
      input_files: maf_filter/analyst_file
    out:
      [output_file]

  copy_number:
    # run some copy number analysis on the data
    run: copy_number.cwl
    in:
      portal_CNA_file: portal_CNA_file
      targets_list: targets_list
      hisens_cncfs: hisens_cncfs
    out: [output_portal_CNA_file]

  copy_cna_file:
    # we need this extra CWL in order to run 'cp' to output a renamed version of the CNA file for cBioPortal
    run: cp.cwl
    in:
      input_file: copy_number/output_portal_CNA_file
      output_filename: analysis_gene_cna_file
    out:
      [output_file]

  rename_analyst_file:
    # we need to use this extra CWL in order to run 'cp' to output a renamed version of the analyst_file
    run: cp.cwl
    in:
      input_file: concat_maf/output_file
      output_filename: analyst_file
    out:
      [output_file]

outputs:
  analyst_file:
    type: File
    outputSource: rename_analyst_file/output_file
  output_portal_CNA_file:
    type: File
    outputSource: copy_number/output_portal_CNA_file
  analysis_gene_cna_file:
    type: File
    outputSource: copy_cna_file/output_file
