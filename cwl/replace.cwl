#!/usr/bin/env cwl-runner

# replace strings in file

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ 'sed', 's/ILLOGICAL/NA/g' ]

requirements:
  DockerRequirement:
    dockerPull: mskcc/helix_filters_01:20.06.2

stdout: $(inputs.output_filename)

inputs:
  input_file:
    type: File
    inputBinding:
      position: 1
  output_filename:
    type: ["null", string]
    default: "output.txt"

outputs:
  output_file:
    type: stdout
