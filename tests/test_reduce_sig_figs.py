#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for reduce_sig_figs.py
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

script = os.path.join(BIN_DIR, 'reduce_sig_figs_seg.mean.py')

class TestReduceSigFigs(PlutoTestCase):
    def setUp(self):
        super().setUp()
        # make a dummy file with some lines
        self.input_lines = ["seg.mean", "3.141592", "2.718281828"]
        self.input_file = os.path.join(self.tmpdir, "input.txt")
        with open(self.input_file, "w") as fout:
            for line in self.input_lines:
                fout.write(line + '\n')

    def test_reduce_sig_figs(self):
        """
        Test that significant figures are reduced correctly
        """
        command = [script, self.input_file]
        returncode, proc_stdout, proc_stderr = self.run_command(command, testcase = self, validate = True)
        lines = proc_stdout.split()
        expected_lines = ['seg.mean', '3.1416', '2.7183']
        self.assertEqual(lines, expected_lines)

if __name__ == "__main__":
    unittest.main()
