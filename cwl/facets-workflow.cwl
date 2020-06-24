#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
doc: "
Workflow for running Facets-suite on a set of tumor normal pairs
"

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
