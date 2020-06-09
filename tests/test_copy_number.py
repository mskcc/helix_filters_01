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
    from .settings import CWL_DIR, CWL_ARGS, DATA_SETS, PORTAL_CNA_FILE

if __name__ == "__main__":
    from tools import run_command
    from settings import CWL_DIR, CWL_ARGS, DATA_SETS, PORTAL_CNA_FILE

cwl_file = os.path.join(CWL_DIR, 'copy_number.cwl')

class TestCopyNumber(unittest.TestCase):
    def test_run_copy_number_one_file(self):
        """
        Test that Facets geneLevel copy number analysis step runs as expected with a single input file
        """
        with TemporaryDirectory() as tmpdir:
            output_dir = os.path.join(tmpdir, "output")
            input_json = {
                "output_cna_filename": "data_CNA.txt",
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
            with open(input_json_file, "w") as input_json_file_data:
                json.dump(input_json, input_json_file_data)

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
                'output_cna_file': {
                    'location': 'file://' + os.path.join(output_dir, "data_CNA.txt"),
                    'basename': "data_CNA.txt",
                    'class': 'File',
                    'checksum': 'sha1$7cc89d24556de93b9a409812317581e67e5df494',
                    'size': 87905,
                    'path': os.path.join(output_dir, "data_CNA.txt")
                },
                'output_cna_ascna_file': {
                    'location': 'file://' + os.path.join(output_dir, "data_CNA.ascna.txt"),
                    'basename': "data_CNA.ascna.txt",
                    'class': 'File',
                    'checksum': 'sha1$452d5ddef12a44693d5a98a05f5d300801734cfe',
                    'size': 6164,
                    'path': os.path.join(output_dir, "data_CNA.ascna.txt")
                },
                'output_cna_scna_file': {
                    'location': 'file://' + os.path.join(output_dir, "data_CNA.scna.txt"),
                    'basename': "data_CNA.scna.txt",
                    'class': 'File',
                    'checksum': 'sha1$8bec923ab1d622b4cf38ae042ac2416725650aed',
                    'size': 5463,
                    'path': os.path.join(output_dir, "data_CNA.scna.txt")
                }
            }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

    def test_run_copy_number_two_files(self):
        """
        Test that Facets geneLevel copy number analysis step runs as expected with two input files
        """
        with TemporaryDirectory() as tmpdir:
            output_dir = os.path.join(tmpdir, "output")
            input_json = {
                "portal_CNA_file": "data_CNA.txt",
                "targets_list" : {
                    "class": "File",
                    "path": DATA_SETS['Proj_08390_G']['targets_list'],
                },
                "hisens_cncfs": [
                    {
                        "class": "File",
                        "path": os.path.join(DATA_SETS['Proj_08390_G']['FACETS_DIR'], "Sample2.rg.md.abra.printreads__Sample1.rg.md.abra.printreads_hisens.cncf.txt")
                    },
                    {
                        "class": "File",
                        "path": os.path.join(DATA_SETS['Proj_08390_G']['FACETS_DIR'], "Sample9.rg.md.abra.printreads__Sample10.rg.md.abra.printreads_hisens.cncf.txt")
                    }
                ],
            }
            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as input_json_file_data:
                json.dump(input_json, input_json_file_data)

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
                'output_cna_file': {
                    'location': 'file://' + os.path.join(output_dir, "data_CNA.txt"),
                    'basename': "data_CNA.txt",
                    'class': 'File',
                    'checksum': 'sha1$6dfa53b8a0fad1156060476bcf445d959f0e6eb2',
                    'size': 143118,
                    'path': os.path.join(output_dir, "data_CNA.txt")
                },
                'output_cna_ascna_file': {
                    'location': 'file://' + os.path.join(output_dir, "data_CNA.ascna.txt"),
                    'basename': "data_CNA.ascna.txt",
                    'class': 'File',
                    'checksum': 'sha1$3953e55b3db85b69209982211c53b9d8f049dc01',
                    'size': 8658,
                    'path': os.path.join(output_dir, "data_CNA.ascna.txt")
                },
                'output_cna_scna_file': {
                    'location': 'file://' + os.path.join(output_dir, "data_CNA.scna.txt"),
                    'basename': "data_CNA.scna.txt",
                    'class': 'File',
                    'checksum': 'sha1$9ddcee42cce0d49aec5745303be480b6c4ef0fe8',
                    'size': 6937,
                    'path': os.path.join(output_dir, "data_CNA.scna.txt")
                }
            }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

if __name__ == "__main__":
    unittest.main()
