#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Reduce the significant figures in the 'seg.mean' column of an input file
"""
import csv
import sys
args = sys.argv[1:]
input_file = args[0]

with open(input_file) as fin:
    reader = csv.DictReader(fin, delimiter = '\t');
    writer = csv.DictWriter(sys.stdout, fieldnames = reader.fieldnames, delimiter = '\t')
    writer.writeheader()
    for row in reader:
        row['seg.mean'] = '%.4f'%float(row['seg.mean'])
        writer.writerow(row)
