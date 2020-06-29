#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the annotate-maf-wrapper.cwl file
"""
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile


# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command
    from .settings import CWL_DIR, CWL_ARGS, DATA_SETS

if __name__ == "__main__":
    from tools import run_command
    from settings import CWL_DIR, CWL_ARGS, DATA_SETS

cwl_file = os.path.join(CWL_DIR, 'annotate-maf-wrapper.cwl')

class TestAnnotateMafWrapperCWL(unittest.TestCase):
    def test_run_facets_wrapper(self):
        """
        """
        input_maf = os.path.join(DATA_SETS['Proj_08390_G']['MAF_DIR'], "Sample1.Sample2.muts.maf")
        input_rds = os.path.join(DATA_SETS['Proj_08390_G']['FACETS_SUITE_DIR'], "Sample1.Sample2_hisens.rds")
        input_json = {
            "maf_file": {
                "path": input_maf,
                "class": "File"
            },
            "facets_rds": {
                "path": input_rds,
                "class": "File"
            },
            "output_filename": "Sample1.Sample2_hisens.ccf.maf"
        }
        with TemporaryDirectory() as tmpdir:
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as json_out:
                json.dump(input_json, json_out)

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

            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'Sample1.Sample2_hisens.ccf.maf'),
                    'basename': 'Sample1.Sample2_hisens.ccf.maf',
                    'class': 'File',
                    'checksum': 'sha1$7e478a8a44d27735f26e368989c672ed6ef5d52a',
                    'size': 19217199,
                    'path': os.path.join(output_dir, 'Sample1.Sample2_hisens.ccf.maf')
                }
            }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

if __name__ == "__main__":
    unittest.main()
