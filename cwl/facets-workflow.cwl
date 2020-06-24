#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
doc: '
Workflow for running Facets-suite on a set of tumor normal pairs


input JSON format;

{
  "pairs": [
    {
      "tumor_bam": {
        "class": "File",
        "path": "/test_data/bam/s_C_ABCD_P001_d.rg.md.abra.printreads.bam"
      },
      "normal_bam": {
        "class": "File",
        "path": "/test_data/bam/s_C_ABCD_N001_d.rg.md.abra.printreads.bam"
      },
      "pair_id": "s_C_ABCD_P001_d.s_C_ABCD_N001_d"
    }
  ]
}
'

inputs:
  pairs:
    type:
      type: array
      items:
        type: record
        fields:
          tumor_bam: File
          normal_bam: File
          pair_id: string

steps: []

outputs: []
