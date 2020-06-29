#!/usr/bin/env cwl-runner

# $ concat_with_comments.sh comment_label comment_value output.txt input1.txt input2.txt ... inputn.txt

cwlVersion: v1.0
class: CommandLineTool
baseCommand: [ 'concat_with_comments.sh' ]

inputs:
  comment_label:
    type: ["null", string]
    default: "helix_filters_01"
    inputBinding:
      position: 1
  comment_value:
    type: string
    inputBinding:
      position: 2
  output_filename:
    type: ["null", string]
    default: "output.txt"
    inputBinding:
      position: 3
  input_files:
    type: File[]
  inputs_file_arg:
    type: ["null", string]
    default:
      valueFrom: ${ return inputs.input_files.map(file => file.path).join(' ') }
    inputBinding:
      position: 4

outputs: []
