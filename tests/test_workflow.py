#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for the workflow.cwl
"""
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile
from .tools import run_command
from .settings import CWL_DIR, CWL_ARGS, DATA_SETS

cwl_file = os.path.join(CWL_DIR, 'workflow.cwl')

class TestWorkflow(unittest.TestCase):
    def test_run_worflow_one_maf(self):
        """
        Test that the workflow works correctly when run with a single maf
        """
        input_json_file = os.path.join(DATA_SETS['Proj_08390_G']['DIR'], "input.one_maf.json")

        with TemporaryDirectory() as tmpdir:

            output_dir = os.path.join(tmpdir, "output")
            tmp_dir = os.path.join(tmpdir, "tmp")
            cache_dir = os.path.join(tmpdir, "cache")

            command = [
                "cwl-runner",
                *CWL_ARGS,
                "--outdir", output_dir,
                "--tmpdir-prefix", tmp_dir,
                "--cachedir", cache_dir,
                cwl_file, input_json_file
                ]

            returncode, proc_stdout, proc_stderr = run_command(command)
            # print(returncode, proc_stdout, proc_stderr)
            output_json = json.loads(proc_stdout)

            self.assertEqual(returncode, 0)

            expected_output = {
                'analysis_dir': {
                    'class': 'Directory',
                    'basename': 'analysis',
                    'listing': [
                        {
                        'location': 'file://' + os.path.join(output_dir, 'analysis/Proj_08390_G.muts.maf'),
                        'basename': 'Proj_08390_G.muts.maf',
                        'class': 'File',
                        'checksum': 'sha1$7a1dbde2f538e72d1dcb9baa7def46922e7454d9',
                        'size': 27901,
                        'path': os.path.join(output_dir, 'analysis/Proj_08390_G.muts.maf')
                        },
                        {
                        'location': 'file://' + os.path.join(output_dir, 'analysis/Proj_08390_G.gene.cna.txt'),
                        'basename': 'Proj_08390_G.gene.cna.txt',
                        'class': 'File',
                        'checksum': 'sha1$ab17d587ad5ae0a87fd6c6d4dd2d5d1701208ce9',
                        'size': 173982,
                        'path': os.path.join(output_dir, 'analysis/Proj_08390_G.gene.cna.txt')
                        }],
                'location': 'file://' + os.path.join(output_dir, 'analysis'),
                'path': os.path.join(output_dir, 'analysis')
                },
                'portal_dir': {
                    'class': 'Directory',
                    'basename': 'portal',
                    'listing': [
                        {'location': 'file://' + os.path.join(output_dir, 'portal/data_CNA.txt'),
                        'basename': 'data_CNA.txt',
                        'class': 'File',
                        'checksum': 'sha1$ab17d587ad5ae0a87fd6c6d4dd2d5d1701208ce9',
                        'size': 173982,
                        'path': os.path.join(output_dir, 'portal/data_CNA.txt')
                        }],
                    'location': 'file://' + os.path.join(output_dir,'portal'),
                    'path': os.path.join(output_dir, 'portal')
                    }
                }

            self.assertDictEqual(output_json, expected_output)
