#!/bin/bash
set -eu

# This script will concatenate table files, preserving the unique comment lines from all input files and adding a new comment line
#
# USAGE:
# $ concat_with_comments.sh comment_label comment_value output.txt input1.txt input2.txt ... inputn.txt
#
# EXAMPLE:
# $ bin/concat_with_comments.sh helix_filters_01 concat-with-comments-0-ga478e4e output.txt ../test_data/maf/*.muts.maf

comment_key="${1}"
comment_value="${2}"
output_file="${3}"
shift
shift
shift

# all the remaining args should be filenames
input_files=( "$@" )
# echo ${input_files[@]}

# get the unique header lines from all files
old_comment_lines="$(grep --no-filename '#' ${input_files[@]} | sort -u)"
printf "%s\n" "$old_comment_lines" > "$output_file"

# make new comment line
new_comment_line="#${comment_key}: ${comment_value}"
echo "${new_comment_line}" >> "$output_file"

# add the header line from the first file
grep -v '#' ${input_files[0]} | head -1 >> "$output_file"

# get all the non-comment, non-header lines from all files
for i in ${input_files[@]}; do
    grep -v '#' "$i" | tail -n +2 >> "$output_file"
done
