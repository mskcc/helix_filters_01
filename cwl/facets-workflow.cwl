#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
doc: '
Workflow for running Facets-suite on a set of tumor normal pairs

This workflow scatters over all the pairs in the input JSON to run all samples in parallel

Input JSON format
-----------------

{
  "pairs": [
    {
      "tumor_bam": {
        "class": "File",
        "path": "/test_data/bam/Tumor1.rg.md.abra.printreads.bam"
      },
      "normal_bam": {
        "class": "File",
        "path": "/test_data/bam/Normal1.rg.md.abra.printreads.bam"
      },
      "pair_maf": {
        "class": "File",
        "path": "/test_data/bam/Tumor1.Normal1.maf"
      },
      "pair_id": "Tumor1.Normal1"
    },
    {
      "tumor_bam": {
        "class": "File",
        "path": "/test_data/bam/Tumor2.rg.md.abra.printreads.bam"
      },
      "normal_bam": {
        "class": "File",
        "path": "/test_data/bam/Normal2.rg.md.abra.printreads.bam"
      },
      "pair_maf": {
        "class": "File",
        "path": "/test_data/bam/Tumor2.Normal2.maf"
      },
      "pair_id": "Tumor2.Normal2"
    }
  ]
}


Output format
-------------

output
└── facets-suite
  ├── Tumor1.Normal1.arm_level.txt
  ├── Tumor1.Normal1.gene_level.txt
  ├── Tumor1.Normal1_hisens.ccf.maf
  ├── Tumor1.Normal1_hisens.rds
  ├── Tumor1.Normal1_hisens.seg
  ├── Tumor1.Normal1_purity.rds
  ├── Tumor1.Normal1_purity.seg
  ├── Tumor1.Normal1.qc.txt
  ├── Tumor1.Normal1.snp_pileup.gz
  ├── Tumor1.Normal1.txt
  ├── Tumor2.Normal2.arm_level.txt
  ├── Tumor2.Normal2.gene_level.txt
  ├── Tumor2.Normal2_hisens.ccf.maf
  ├── Tumor2.Normal2_hisens.rds
  ├── Tumor2.Normal2_hisens.seg
  ├── Tumor2.Normal2_purity.rds
  ├── Tumor2.Normal2_purity.seg
  ├── Tumor2.Normal2.qc.txt
  ├── Tumor2.Normal2.snp_pileup.gz
  └── Tumor2.Normal2.txt
'

requirements:
  ScatterFeatureRequirement: {}
  InlineJavascriptRequirement: {}
  StepInputExpressionRequirement: {}
  SubworkflowFeatureRequirement: {}

inputs:
  pairs:
    type:
      type: array
      items:
        type: record
        fields:
          tumor_bam: File
          normal_bam: File
          pair_maf: File
          pair_id: string
  snps_vcf:
    type: File

steps:
  facets_suite:
    run: facets-suite-workflow.cwl
    scatter: pair
    in:
      pair: pairs
      snps_vcf: snps_vcf
      tumor_bam:
        valueFrom: ${ return inputs.pair['tumor_bam']; }
      normal_bam:
        valueFrom: ${ return inputs.pair['normal_bam']; }
      pair_maf:
        valueFrom: ${ return inputs.pair['pair_maf']; }
      pair_id:
        valueFrom: ${ return inputs.pair['pair_id']; }
    out:
      [
      pair_id,
      snp_pileup,
      purity_seg,
      hisens_seg,
      qc_txt,
      gene_level_txt,
      arm_level_txt,
      facets_txt,
      purity_rds,
      hisens_rds,
      annotated_maf
      ]


outputs:
  snp_pileup:
    type:
      type: array
      items: File
    outputSource: facets_suite/snp_pileup
  purity_seg:
    type:
      type: array
      items: File
    outputSource: facets_suite/purity_seg
  hisens_seg:
    type:
      type: array
      items: File
    outputSource: facets_suite/hisens_seg
  qc_txt:
    type:
      type: array
      items: File
    outputSource: facets_suite/qc_txt
  gene_level_txt:
    type:
      type: array
      items: File
    outputSource: facets_suite/gene_level_txt
  arm_level_txt:
    type:
      type: array
      items: File
    outputSource: facets_suite/arm_level_txt
  facets_txt:
    type:
      type: array
      items: File
    outputSource: facets_suite/facets_txt
  purity_rds:
    type:
      type: array
      items: File
    outputSource: facets_suite/purity_rds
  hisens_rds:
    type:
      type: array
      items: File
    outputSource: facets_suite/hisens_rds
  annotated_maf:
    type:
      type: array
      items: File
    outputSource: facets_suite/annotated_maf
