#!/usr/bin/env cwl-runner

# run-facets-wrapper.R \
# --counts-file $${snp_pileup} \
# --sample-id $${pair_id} \
# --purity-cval 100 \
# --cval 50 \
# --seed 1000 \
# --everything \
# --min-nhet 25 \
# --purity-min-nhet 25 \
# -D $(FACETS_OUTPUT) \
# --facets-lib-path /usr/local/lib/R/site-library

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ['run-facets-wrapper.R', '--everything', '-D', '.', '--facets-lib-path', '/usr/local/lib/R/site-library']

requirements:
  DockerRequirement:
    dockerPull: stevekm/facets-suite:dev

inputs:
  snp_pileup:
    type: File
    inputBinding:
      position: 1
      prefix: '--counts-file'
  sample_id:
    type: string
    inputBinding:
      position: 2
      prefix: '--sample-id'
  purity_cval:
    type: ["null", string]
    default: "100"
    inputBinding:
      position: 3
      prefix: '--purity-cval'
  cval:
    type: ["null", string]
    default: "50"
    inputBinding:
      position: 4
      prefix: '--cval'
  seed:
    type: ["null", string]
    default: "1000"
    inputBinding:
      position: 5
      prefix: '--seed'
  min_nhet:
    type: ["null", string]
    default: "25"
    inputBinding:
      position: 6
      prefix: '--min-nhet'
  purity_min_nhet:
    type: ["null", string]
    default: "25"
    inputBinding:
      position: 7
      prefix: '--purity-min-nhet'

# s_C_ABCD_P001_d_s_C_ABCD_N001_d_purity.seg
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_purity.png
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.seg
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.png
# s_C_ABCD_P001_d_s_C_ABCD_N001_d.qc.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d.gene_level.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d.arm_level.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_purity.rds
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.rds
outputs:
  purity_seg:
    type: File
    outputBinding:
      glob: $(inputs.sample_id)_purity.seg
  hisens_seg:
    type: File
    outputBinding:
      glob: $(inputs.sample_id)_hisens.seg
  qc_txt:
    type: File
    outputBinding:
      glob: $(inputs.sample_id).qc.txt
  gene_level_txt:
    type: File
    outputBinding:
      glob: $(inputs.sample_id).gene_level.txt
  arm_level_txt:
    type: File
    outputBinding:
      glob: $(inputs.sample_id).arm_level.txt
  output_txt:
    type: File
    outputBinding:
      glob: $(inputs.sample_id).txt
  purity_rds:
    type: File
    outputBinding:
      glob: $(inputs.sample_id)_purity.rds
  hisens_rds:
    type: File
    outputBinding:
      glob: $(inputs.sample_id)_hisens.rds
