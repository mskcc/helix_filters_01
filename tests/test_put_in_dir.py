#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for the put_in_dir.cwl
"""
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile
from .tools import run_command
from .settings import CWL_DIR, CWL_ARGS

cwl_file = os.path.join(CWL_DIR, 'put_in_dir.cwl')

class TestPutInDir(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        setUp class for the tests; this will only execute once and will be available for
        the tests to access the results
        """
        super(TestPutInDir, cls).setUpClass()
        # cls.flagstat = flagstat.Flagstat(txt = demo_flagstat)

    def test_put_two_files_in_dir(self):
        """
        """
        with TemporaryDirectory() as tmpdir, NamedTemporaryFile() as file1, NamedTemporaryFile() as file2:
            # set path to the dir which this CWL should to output to
            output_dir = os.path.join(tmpdir, "output")

            # create input data
            input_json = {
                "output_directory_name": output_dir,
                "files": [
                    {
                      "class": "File",
                      "path": file1.name
                    },
                    {
                      "class": "File",
                      "path": file2.name
                    }
                ]
            }

            # write input data
            input_json_file = os.path.join(tmpdir, "input.json")
            json.dump(input_json, open(input_json_file, "w"))

            # command args to run CWL
            command = [ "cwl-runner", *CWL_ARGS, cwl_file, input_json_file ]

            # run the command
            returncode, proc_stdout, proc_stderr = run_command(command)

            # test that command ran successfully
            self.assertEqual(returncode, 0)

            # parse the stdout
            output_json = json.loads(proc_stdout)

            # make sure the output is a dir
            self.assertTrue("directory" in output_json)
            # make sure there's only one element output
            self.assertEqual(len(output_json), 1)
            # make sure the dir exists
            self.assertTrue(os.path.exists( output_json['directory']['path'] ))
            self.assertTrue(os.path.isdir( output_json['directory']['path'] ))
            self.assertEqual(output_dir, output_json['directory']['path'])
            # make sure both files were output to the dir
            self.assertEqual(len(os.listdir(output_json['directory']['path'])), 2)
            self.assertTrue(os.path.basename(file1.name)in os.listdir(output_json['directory']['path']) )
            self.assertTrue(os.path.basename(file2.name)in os.listdir(output_json['directory']['path']) )