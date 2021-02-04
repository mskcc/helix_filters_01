#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests cases for calculating TMB tumor mutational burden values
"""
import os
import sys
import unittest

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)
from pluto.tools import PlutoTestCase
from settings import BIN_DIR
sys.path.pop(0)


script = os.path.join(BIN_DIR, 'calc-tmb.py')

class TestCalcTMB(PlutoTestCase):
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
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)
        # print(proc_stdout, proc_stderr)
        result = proc_stdout
        expected_result = '0.000001115278535237783'
        self.assertEqual(result, expected_result)

        # get result as TMB in Megabases
        command = [script, 'from-values', '--num-variants', "1", '--genome-coverage', "896637"]
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)
        result = proc_stdout
        expected_result = '0.000000000001115278535237783'
        self.assertEqual(result, expected_result)

        command = [script, 'from-values', '--num-variants', "10001", '--genome-coverage', "1213770"]
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)
        result = proc_stdout
        expected_result = '0.00000000823961706089292'
        self.assertEqual(result, expected_result)

        # save output to file
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, 'from-values', '--num-variants', "10001", '--genome-coverage', "1213770", '--output-file', output_file, '--no-print']
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)
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
        input_maf_file = self.write_table(tmpdir = self.tmpdir, filename = 'input.maf', lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, 'from-file', input_maf_file, output_file, '--genome-coverage', "1000"]
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)
        with open(output_file) as fin:
            result = next(fin).strip()
        expected_result = '0.000000005'
        self.assertEqual(result, expected_result)

    def test_calc_tmb_from_file2(self):
        """
        Test case for calculating TMB by reading the number of variants from a file

        This test case is for some weird edge cases
        """
        # One variant in the file
        maf_lines = [
            ['Hugo_Symbol', 'Chromosome'],
            ['SUFU', '1'],
        ]
        input_maf_file = self.write_table(tmpdir = self.tmpdir, filename = 'input.maf', lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, 'from-file', input_maf_file, output_file, '--genome-coverage', "1000"]
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)
        with open(output_file) as fin:
            result = next(fin).strip()
        expected_result = '0.000000001'
        self.assertEqual(result, expected_result)

        # No variants in the file
        maf_lines = [
            ['Hugo_Symbol', 'Chromosome'],
        ]
        input_maf_file = self.write_table(tmpdir = self.tmpdir, filename = 'input.maf', lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, 'from-file', input_maf_file, output_file, '--genome-coverage', "1000"]
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)
        with open(output_file) as fin:
            result = next(fin).strip()
        expected_result = '0.0'
        self.assertEqual(result, expected_result)


        # completely empty file; script will break
        maf_lines = []
        input_maf_file = self.write_table(tmpdir = self.tmpdir, filename = 'input.maf', lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")
        command = [script, 'from-file', input_maf_file, output_file, '--genome-coverage', "1000"]
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = False, testcase = self)
        self.assertEqual(returncode, 1)

    def test_check_normal_id(self):
        """
        To facilitate pipeline usage, we should not calculate TMB on a tumor that was paired to a Pooled Normal sample
        So add some extra options to the calc-tmb.py script to supply a normal sample id, check the id if it matches "poolednormal",
        and if so, output NA instead of the TMB value
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
        input_maf_file = self.write_table(tmpdir = self.tmpdir, filename = 'input.maf', lines = maf_lines)
        output_file = os.path.join(self.tmpdir, "output.txt")

        # with a good normal ID; not a pooled normal
        command = [script, 'from-file', input_maf_file, output_file, '--genome-coverage', "1000", "--normal-id", "foo"]
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)
        with open(output_file) as fin:
            result = next(fin).strip()
        expected_result = '0.000000005'
        self.assertEqual(result, expected_result)

        # with a bad normal id
        command = [script, 'from-file', input_maf_file, output_file, '--genome-coverage', "1000", "--normal-id", "ABCPOOLEDNORMAL123"]
        returncode, proc_stdout, proc_stderr = self.run_command(command, validate = True, testcase = self)
        with open(output_file) as fin:
            result = next(fin).strip()
        expected_result = 'NA'
        self.assertEqual(result, expected_result)





if __name__ == "__main__":
    unittest.main()
