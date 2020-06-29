#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ tail ]
requirements:
  DockerRequirement:
    dockerPull: mskcc/helix_filters_01:20.06.2
stdout: $(inputs.input_file.basename).tail.txt
inputs:
  num_lines:
    type: string
    inputBinding:
      prefix: -n
      position: 1
  input_file:
    type: File
    inputBinding:
      position: 2
outputs:
  output_file:
    type: stdout
