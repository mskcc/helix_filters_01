#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ "generate_cbioPortal_files.py" ]

inputs:
  subcommand:
    type: string
    inputBinding:
      position: 1
  output_filename:
    type: string
    inputBinding:
      prefix: '--output'
      position: 2
  cancer_study_id:
    type: ['null', string]
    inputBinding:
      prefix: '--cancer-study-id'
      position: 3
  sample_data_filename:
    type: ['null', string]
    inputBinding:
      prefix: '--sample-data-filename'
      position: 4


outputs:
  output_file:
    type: File
    outputBinding:
      glob: $(inputs.output_filename)
