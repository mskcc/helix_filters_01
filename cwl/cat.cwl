#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ cat ]
requirements:
  DockerRequirement:
    dockerPull: mskcc/helix_filters_01:20.06.2
stdout: output.txt
inputs:
  input_files:
    type: File[]
    inputBinding:
      position: 1
outputs:
  output_file:
    type: stdout
