#!/usr/bin/env cwl-runner

# snp-pileup-wrapper.R \
# --vcf-file $(FACETS_SNPS_VCF) \
# --normal-bam $${normal_bam} \
# --tumor-bam $${tumor_bam} \
# --output-prefix "$${snp_prefix}"

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ['snp-pileup-wrapper.R']

requirements:
  DockerRequirement:
    dockerPull: stevekm/facets-suite:dev

inputs:
  snps_vcf:
    type: File
    inputBinding:
      position: 1
      prefix: '--vcf-file'
  normal_bam:
    type: File
    inputBinding:
      position: 2
      prefix: '--normal-bam'
  tumor_bam:
    type: File
    inputBinding:
      position: 3
      prefix: '--tumor-bam'
  output_prefix:
    type: string
    inputBinding:
      position: 4
      prefix: '--output-prefix'

outputs:
  output_file:
    type: File
    outputBinding:
      glob: $(inputs.output_prefix).snp_pileup.gz
