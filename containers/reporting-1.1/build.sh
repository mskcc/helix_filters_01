#!/bin/bash
# script to build the R container because it needs the scripts from the bin dir
[ -e report ] && rm -rf report
cp -r ../../report .
docker build -t "mskcc/helix_filters_01:reporting-1.1" .
