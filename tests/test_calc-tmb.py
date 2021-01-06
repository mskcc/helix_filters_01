#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cases for calculating TMB tumor mutational burden values
"""
import os
import sys
import unittest
from tools import TmpDirTestCase, run_command, write_table
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
    def test_calc_tmb_from_values(self):
        """
        Test cases for calling the TMB script with only values and checking results

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

        # save output to file
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, 'from-values', '--num-variants', "10001", '--genome-coverage', "1213770", '--output-file', output_file, '--no-print']
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)
        # stdout should be empty
        expected_stdout = ''
        self.assertEqual(proc_stdout, expected_stdout)
        # value should be in the file
        with open(output_file) as fin:
            result = next(fin).strip()
        expected_result = '0.00000000823961706089292'
        self.assertEqual(result, expected_result)

    def test_calc_tmb_from_file(self):
        """
        Test case for calculating TMB by reading the number of variants from a file
        """
        maf_lines = [
            ['# comment 1'],
            ['# comment 2'],
            ['Hugo_Symbol', 'Chromosome'],
            ['SUFU', '1'],
            ['SUFU', '1'],
            ['SUFU', '1'],
            ['SUFU', '1'],
            ['GOT1', '2']
        ]
        input_maf_file = write_table(tmpdir = self.tmpdir, filename = 'input.maf', lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, 'from-file', input_maf_file, output_file, '--genome-coverage', "1000"]
        returncode, proc_stdout, proc_stderr = run_command(command, validate = True, testcase = self)
        with open(output_file) as fin:
            result = next(fin).strip()
        expected_result = '0.000000005'
        self.assertEqual(result, expected_result)





if __name__ == "__main__":
    unittest.main()
