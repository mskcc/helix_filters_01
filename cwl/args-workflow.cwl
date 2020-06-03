#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

requirements:
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}

inputs: []

steps:
  run_args1:
    run: args.cwl
    in:
      args_str:
        valueFrom: ${ return ["foo", "bar", "baz"].join(':'); }
    out:
      [output_file]

  run_args2:
    run: args.cwl
    in:
      input_file: run_args1/output_file
      args_str:
        valueFrom: ${ return ["bazzz", "buzzz"].join(','); }
    out:
      [output_file]

outputs:
  output:
    type: File
    outputSource: run_args2/output_file
