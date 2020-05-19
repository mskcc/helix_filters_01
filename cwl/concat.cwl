#!/usr/bin/env cwl-runner

# concatenate tables; keep the header from the first file, then all lines minus header from all files
#  strip the header comments that start with '#'
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["bash", "concat.sh"]

requirements:
  DockerRequirement:
    dockerPull: mskcc/helix_filters_01:1.0.0
  InlineJavascriptRequirement: {}
  InitialWorkDirRequirement:
    listing:
      - entryname: concat.sh
        entry: |-
          grep -v '#' $(inputs.input_files[0].path) | head -1  > output.txt
          for item in ${
            var output = [];
            for (var i = 0; i < inputs.input_files.length; i++){
              output.push(inputs.input_files[i]['path']);
              };
              return output.join(' ');
              }; do
          grep -v '#' \$item | tail -n +2 >> output.txt
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
