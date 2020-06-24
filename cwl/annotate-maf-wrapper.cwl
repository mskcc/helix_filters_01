#!/usr/bin/env cwl-runner

# annotate-maf-wrapper.R \
# --maf-file $${pair_maf} \
# --facets-output $${facets_rds} \
# -o $${annot_maf}

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ['annotate-maf-wrapper.R']

requirements:
  DockerRequirement:
    dockerPull: stevekm/facets-suite:dev

inputs:
  maf_file:
    type: File
    inputBinding:
      position: 1
      prefix: '--maf-file'
  facets_rds:
    type: File
    inputBinding:
      position: 2
      prefix: '--facets-output'
  output_filename: # $${pair_id}_hisens.ccf.maf
    type: string
    inputBinding:
      position: 3
      prefix: '-o'

outputs:
  output_file:
    type: File
    outputBinding:
      glob: $(inputs.output_filename) # $${pair_id}_hisens.ccf.maf
