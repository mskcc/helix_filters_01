#!/usr/bin/env cwl-runner
# maf_filter.py "${maf}" "${config.version}" "${config.is_impact}" "${analysis_mut_file}" "${portal_file}"
# analysis_mut_file = "${config.project_id}.muts.maf"
#   portal_file = "data_mutations_extended.txt"

cwlVersion: v1.0
class: CommandLineTool
baseCommand: /usr/bin/helix_filters_01/bin/maf_filter.py

requirements:
  DockerRequirement:
    dockerPull: mskcc/helix_filters_01:1.0.0

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
  analyst_filename:
    type: string
    inputBinding:
      position: 4
  portal_filename:
    type: string
    inputBinding:
      position: 5
outputs:
  analyst_file:
    type: File
    outputBinding:
      glob: $(inputs.analyst_filename)
  portal_file:
    type: File
    outputBinding:
      glob: $(inputs.portal_filename)
