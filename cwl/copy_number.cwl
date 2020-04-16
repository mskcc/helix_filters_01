#!/usr/bin/env cwl-runner

# python /usr/bin/facets-suite/facets geneLevel \
#   -o "${portal_CNA_file}" \
#   --cnaMatrix \
#   -f ${items} \
#   --targetFile "${targets_list}"
#
#   cp "${portal_CNA_file}" "${analysis_gene_cna_file}"

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "/usr/bin/facets-suite/facets", "geneLevel", "--cnaMatrix"]

requirements:
  DockerRequirement:
    dockerPull: mskcc/roslin-variant-facets:1.6.3

inputs:
  portal_CNA_file:
    type: string
    inputBinding:
      position: 1
      prefix: -o
  targets_list:
    type: File
    inputBinding:
      position: 2
      prefix: --targetFile
  hisens_cncfs:
    type: File[]
    inputBinding:
      position: 3
      prefix: -f
outputs:
  output_portal_CNA_file:
    type: File
    outputBinding:
      glob: $(inputs.portal_CNA_file)
