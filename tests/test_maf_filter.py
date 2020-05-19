#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for the maf_filter.cwl
"""
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command
    from .settings import CWL_DIR, CWL_ARGS, DATA_SETS, ARGOS_VERSION_STRING, IS_IMPACT, PORTAL_FILE, PORTAL_CNA_FILE

if __name__ == "__main__":
    from tools import run_command
    from settings import CWL_DIR, CWL_ARGS, DATA_SETS, ARGOS_VERSION_STRING, IS_IMPACT, PORTAL_FILE, PORTAL_CNA_FILE

cwl_file = os.path.join(CWL_DIR, 'maf_filter.cwl')

class TestMafFilter(unittest.TestCase):
    def test_filter_a_maf_file(self):
        """
        Test that a filtered maf file comes out as expected
        """
        with TemporaryDirectory() as tmpdir:
            output_dir = os.path.join(tmpdir, "output")
            input_json = {
                "maf_file": {
                      "class": "File",
                      "path": os.path.join(DATA_SETS['Proj_08390_G']['MAF_DIR'], "Sample1.Sample2.muts.maf")
                    },
                "argos_version_string": ARGOS_VERSION_STRING,
                "is_impact": IS_IMPACT,
                "analyst_file": DATA_SETS['Proj_08390_G']['analyst_file'],
                "portal_file": PORTAL_FILE
            }
            input_json_file = os.path.join(tmpdir, "input.json")
            json.dump(input_json, open(input_json_file, "w"))

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
                print(proc_stdout)

            self.assertEqual(returncode, 0)

            output_json = json.loads(proc_stdout)

            expected_output = {
                'analyst_file': {
                    'location': 'file://' + os.path.join(output_dir, DATA_SETS['Proj_08390_G']['analyst_file']),
                    'basename': DATA_SETS['Proj_08390_G']['analyst_file'],
                    'class': 'File',
                    'checksum': 'sha1$49086adcecc296905ed210ce512bf71a56a4e71a',
                    'size': 27917,
                    'path': os.path.join(output_dir, DATA_SETS['Proj_08390_G']['analyst_file'])
                    },
                'portal_file': {
                    'location': 'file://' + os.path.join(output_dir, PORTAL_FILE),
                    'basename': PORTAL_FILE,
                    'class': 'File',
                    'checksum': 'sha1$f35288b7d321e34f17abbcb02e29df942e308601',
                    'size': 4372,
                    'path': os.path.join(output_dir, PORTAL_FILE)
                    }
                }
            self.assertDictEqual(output_json, expected_output)


if __name__ == "__main__":
    unittest.main()
