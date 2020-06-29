#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ "generate_cbioPortal_files.py" ]

requirements:
  DockerRequirement:
    dockerPull: mskcc/helix_filters_01:20.06.2

inputs:
  # required for every invocation
  subcommand:
    type: string
    inputBinding:
      position: 1
  output_filename:
    type: string
    inputBinding:
      prefix: '--output'
      position: 2
  # not required for all invocations
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
  data_clinical_file:
    type: ['null', File]
    inputBinding:
      prefix: '--data-clinical-file'
      position: 5
  sample_summary_file:
    type: ['null', File]
    inputBinding:
      prefix: '--sample-summary-file'
      position: 6
  project_pi:
    type: ['null', string]
    inputBinding:
      prefix: '--project-pi'
      position: 7
  request_pi:
    type: ['null', string]
    inputBinding:
      prefix: '--request-pi'
      position: 8
  name:
    type: ['null', string]
    inputBinding:
      prefix: '--name'
      position: 9
  short_name:
    type: ['null', string]
    inputBinding:
      prefix: '--short-name'
      position: 10
  type_of_cancer:
    type: ['null', string ]
    inputBinding:
      prefix: '--type-of-cancer'
      position: 11
  extra_groups: # TODO: figure out how to pass more than one group here
    type: ['null', string ]
    inputBinding:
      prefix: '--extra-groups'
      position: 12
  patient_data_filename:
    type: ['null', string ]
    inputBinding:
      prefix: '--patient-data-filename'
      position: 13
  cna_data_filename:
    type: ['null', string ]
    inputBinding:
      prefix: '--cna-data-filename'
      position: 14
  fusion_data_filename:
    type: ['null', string ]
    inputBinding:
      prefix: '--fusion-data-filename'
      position: 16
  mutations_data_filename:
    type: ['null', string ]
    inputBinding:
      prefix: '--mutations-data-filename'
      position: 17
  segmented_data_filename:
    type: ['null', string ]
    inputBinding:
      prefix: '--segmented-data-file'
      position: 18
  description:
    type: ['null', string ]
    inputBinding:
      prefix: '--description'
      position: 19



outputs:
  output_file:
    type: File
    outputBinding:
      glob: $(inputs.output_filename)
