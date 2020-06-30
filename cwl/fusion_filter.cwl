#!/usr/bin/env cwl-runner

# fusion_filter.py concatenated_fusions.txt "data_fusions.txt" "$(KNOWN_FUSIONS_FILE)"

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["fusion_filter.py"]

requirements:
  DockerRequirement:
    dockerPull: mskcc/helix_filters_01:20.06.2

inputs:
  fusions_file:
    type: File
    inputBinding:
      position: 1
  output_filename:
    type: ["null", string]
    default: data_fusions.txt
    inputBinding:
      position: 2
  known_fusions_file:
    type: File
    inputBinding:
      position: 3

outputs:
  output_file:
    type: File
    outputBinding:
      glob: $(inputs.output_filename)
