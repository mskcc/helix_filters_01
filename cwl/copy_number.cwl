#!/usr/bin/env cwl-runner

# python /usr/bin/facets-suite/facets geneLevel \
#   -o "${portal_CNA_file}" \
#   --cnaMatrix \
#   -f ${items} \
#   --targetFile "${targets_list}"
#
#   cp "${portal_CNA_file}" "${analysis_gene_cna_file}"

# NOTE: Beware of massive CLI arg lists with large amounts of files

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python", "/usr/bin/facets-suite/facets", "geneLevel", "--cnaMatrix"]

requirements:
  DockerRequirement:
    dockerPull: mskcc/roslin-variant-facets:1.6.3

inputs:
  output_cna_filename:
    type: ["null", string]
    default: "data_CNA.txt"
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
  output_cna_ascna_filename:
    type: ["null", string]
    default: "data_CNA.ascna.txt"
  output_cna_scna_filename:
    type: ["null", string]
    default: "data_CNA.scna.txt"
outputs:
  output_cna_file:
    type: File
    outputBinding:
      glob: $(inputs.output_cna_filename)
  output_cna_ascna_file:
    type: File
    outputBinding:
      glob: $(inputs.output_cna_ascna_filename)
  output_cna_scna_file:
    type: File
    outputBinding:
      glob: $(inputs.output_cna_scna_filename)
