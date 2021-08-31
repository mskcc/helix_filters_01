#!/bin/bash
# script to build the R container because it needs the scripts from the bin dir
[ -e bin ] && rm -rf bin
cp -r ../../bin .
docker build -t "mskcc/helix_filters_01:R-3.5.1" .
