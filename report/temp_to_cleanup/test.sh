IFS=$'\n' read -d '' -r -a lines < ../../sample_project_paths

# all lines
echo "${lines[@]}"
