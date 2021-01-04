#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cases for calculating TMB tumor mutational burden values
"""
import os
import sys
import unittest
from tools import TmpDirTestCase, run_command, write_table, load_mutations, dicts2lines
from settings import BIN_DIR

script = os.path.join(BIN_DIR, 'calc-tmb.py')

class TestCalcTMB(TmpDirTestCase):
    """
    Assays
    ------
    IMPACTv3: 896,637
    IMPACTv5: 1,016,335
    IMPACTv6: 1,139,294
    IMPACTv7: 1,213,770
    """
    def test_calc_tmb_script(self):
        """
        Test cases for calling the TMB script and checking results

        >>> from numpy import format_float_positional
        >>> x = 1 / 896637
        >>> format_float_positional(x)
        '0.000001115278535237783'
        """
        # get result as TMB in bases
        command = [script, 'from-values', '--num-variants', "1", '--genome-coverage', "896637", '--raw']
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)
        # print(proc_stdout, proc_stderr)
        result = proc_stdout
        expected_result = '0.000001115278535237783'
        self.assertEqual(result, expected_result)

        # get result as TMB in Megabases
        command = [script, 'from-values', '--num-variants', "1", '--genome-coverage', "896637"]
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)
        result = proc_stdout
        expected_result = '0.000000000001115278535237783'
        self.assertEqual(result, expected_result)

        command = [script, 'from-values', '--num-variants', "10001", '--genome-coverage', "1213770"]
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)
        result = proc_stdout
        expected_result = '0.00000000823961706089292'
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
