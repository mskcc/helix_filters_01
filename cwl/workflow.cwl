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

outputs: []
