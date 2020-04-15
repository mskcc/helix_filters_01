#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["bash", "concat.sh"]

requirements:
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing:
      - entryname: concat.sh
        entry: |-
          head -1 $(inputs.input_files[1].path) > output.txt
          for i in ${ var output = []; for (var i = 0; i < inputs.input_files.length; i++){ output=output.concat(inputs.input_files[i]['path']); } return output.join(' ');}; do
          tail -n +2 \$i >> output.txt
          done

# echo ${return item['path'] for item in inputs.input_files}
inputs:
  input_files:
    type: File[]

outputs:
  output_file:
    type: File
    outputBinding:
      glob: output.txt
