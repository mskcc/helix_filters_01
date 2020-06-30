#!/usr/bin/env cwl-runner

# concatenate tables; keep the header from the first file, then all lines minus header from all files
#  strip the header comments that start with '#'
cwlVersion: v1.0
class: Workflow

requirements:
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}
  DockerRequirement:
    dockerPull: mskcc/helix_filters_01:20.06.2

# echo ${return item['path'] for item in inputs.input_files}
inputs:
  input_files:
    type: File[]

steps:
  strip_comments:
    run: strip.cwl
    in:
      input_file: input_files
    scatter: [input_file]
    scatterMethod: dotproduct
    out: [output_file]
  get_header:
    run: head.cwl
    in:
      input_files: strip_comments/output_file
      input_file:
        valueFrom: ${ return inputs.input_files[0]; }
      num_lines:
        valueFrom: ${ return "1"; }
    out: [output_file]
  get_data:
    run: tail.cwl
    in:
      input_file: strip_comments/output_file
      num_lines:
        valueFrom: ${ return "+2"; }
    scatter: [input_file]
    scatterMethod: dotproduct
    out: [output_file]
  combine_header_and_data:
    run: cat.cwl
    in:
      header: get_header/output_file
      data_files: get_data/output_file
      input_files:
        valueFrom: ${ var file_list = [inputs.header]; return file_list.concat(inputs.data_files); }
    out: [output_file]
outputs:
  output_file:
    type: File
    outputSource: combine_header_and_data/output_file
