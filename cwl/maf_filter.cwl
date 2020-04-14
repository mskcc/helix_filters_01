#!/usr/bin/env cwl-runner
# maf_filter.py "${maf}" "${config.version}" "${config.is_impact}" "${analysis_mut_file}" "${portal_file}"
# analysis_mut_file = "${config.project_id}.muts.maf"
#   portal_file = "data_mutations_extended.txt"

cwlVersion: v1.0
class: CommandLineTool
baseCommand: maf_filter.py
inputs:
  maf_file:
    type: File
    inputBinding:
      position: 1
  roslin_version_string:
    type: string
    inputBinding:
      position: 2
  is_impact:
    type: string
    inputBinding:
      position: 3
  analyst_file:
    type: string
    inputBinding:
      position: 4
  portal_file:
    type: string
    inputBinding:
      position: 5
outputs:
  analyst_file:
    type: File
    outputBinding:
      glob: $(inputs.analyst_file)
  portal_file:
    type: File
    outputBinding:
      glob: $(inputs.portal_file)
