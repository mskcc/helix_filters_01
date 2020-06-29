#!/usr/bin/env cwl-runner
# maf_filter.py "${maf}" "${config.version}" "${config.is_impact}" "${analysis_mut_file}" "${portal_file}"
# analysis_mut_file = "${config.project_id}.muts.maf"
#   portal_file = "data_mutations_extended.txt"

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ['maf_filter.py']

requirements:
  DockerRequirement:
    dockerPull: mskcc/helix_filters_01:20.06.2

inputs:
  maf_file:
    type: File
    inputBinding:
      position: 1
  argos_version_string:
    type: string
    inputBinding:
      position: 2
  is_impact:
    type: string
    inputBinding:
      position: 3
  analysis_mutations_filename:
    type: string
    inputBinding:
      position: 4
  cbio_mutation_data_filename:
    type: string
    inputBinding:
      position: 5
outputs:
  analysis_mutations_file:
    type: File
    outputBinding:
      glob: $(inputs.analysis_mutations_filename)
  cbio_mutation_data_file:
    type: File
    outputBinding:
      glob: $(inputs.cbio_mutation_data_filename)
