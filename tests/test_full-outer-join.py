#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for the generation of cBio Portal files
"""
import sys
import os
import unittest

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from pluto.tools import PlutoTestCase
from settings import BIN_DIR
sys.path.pop(0)

test_script = os.path.join(BIN_DIR, 'full-outer-join.R')


class TestFullOuterJoinScript(PlutoTestCase):
    def test_full_outer_join1(self):
        lines1 = [
        ['Hugo_Symbol', 'Sample1', 'Sample2'],
        ["TAP1", "0", "0"],
        ["ERRFI1", "0", "0"],
        ["STK19", "", "0"],
        ]

        lines2 = [
        ['Hugo_Symbol', 'Sample3', 'Sample4'],
        ["ERRFI1", "0", "0"],
        ["STK19", "-2", "0"],
        ["STK11", "0", ""],
        ]

        cna_file1 = self.write_table(self.tmpdir, filename = "cna1.txt", lines = lines1)
        cna_file2 = self.write_table(self.tmpdir, filename = "cna2.txt", lines = lines2)
        output_file = os.path.join(self.tmpdir, "output.tsv")

        command = [ test_script, cna_file1, cna_file2, 'Hugo_Symbol', output_file ]
        returncode, proc_stdout, proc_stderr = self.run_command(command, testcase = self, validate = True)

        lines = self.read_table(output_file)

        expected_lines = [
            ['Hugo_Symbol', 'Sample1', 'Sample2', 'Sample3', 'Sample4'],
            ['ERRFI1', '0', '0', '0', '0'],
            ['STK19', 'NA', '0', '-2', '0'],
            ['TAP1', '0', '0', 'NA', 'NA'],
            ['STK11', 'NA', 'NA', '0', 'NA']
            ]
        self.assertEqual(lines, expected_lines)



if __name__ == "__main__":
    unittest.main()
