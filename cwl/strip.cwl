#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ grep, -v, '#' ]
requirements:
  DockerRequirement:
    dockerPull: mskcc/helix_filters_01:20.06.2
stdout: $(inputs.input_file.basename).strip.txt
inputs:
  input_file:
    type: File
    inputBinding:
      position: 1
outputs:
  output_file:
    type: stdout
