#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for the copy_number.cwl
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

cwl_file = os.path.join(CWL_DIR, 'copy_number.cwl')

class TestCopyNumber(unittest.TestCase):
    def test_run_copy_number_one_file(self):
        """
        Test that Facets geneLevel copy number analysis step runs as expected
        """
        with TemporaryDirectory() as tmpdir:
            output_dir = os.path.join(tmpdir, "output")
            input_json = {
                "portal_CNA_file": PORTAL_CNA_FILE,
                "targets_list" : {
                    "class": "File",
                    "path": DATA_SETS['Proj_08390_G']['targets_list'],
                },
                "hisens_cncfs": [
                    {
                        "class": "File",
                        "path": os.path.join(DATA_SETS['Proj_08390_G']['FACETS_DIR'], "Sample2.rg.md.abra.printreads__Sample1.rg.md.abra.printreads_hisens.cncf.txt")
                    }
                ],
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
                'output_portal_CNA_file': {
                    'location': 'file://' + os.path.join(output_dir, PORTAL_CNA_FILE),
                    'basename': PORTAL_CNA_FILE,
                    'class': 'File',
                    'checksum': 'sha1$7cc89d24556de93b9a409812317581e67e5df494',
                    'size': 87905,
                    'path': os.path.join(output_dir, PORTAL_CNA_FILE)
                }
            }
            self.assertDictEqual(output_json, expected_output)

if __name__ == "__main__":
    unittest.main()
