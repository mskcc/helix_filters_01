#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the run-facets-wrapper.cwl file
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

cwl_file = os.path.join(CWL_DIR, 'run-facets-wrapper.cwl')

class TestRunFacetsWrapperCWL(unittest.TestCase):
    def test_run_facets_wrapper(self):
        """
        """
        input_json = {
            "snp_pileup": {
                "path": os.path.join(DATA_SETS['Proj_08390_G']['SNP_PILEUP_DIR'], "Sample24.Sample23.snp_pileup.gz"),
                "class": "File"
            },
            "sample_id": "Sample24.Sample23"
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
                'arm_level_txt': {
                    'location': 'file://' + os.path.join(output_dir, 'Sample24.Sample23.arm_level.txt'),
                    'basename': 'Sample24.Sample23.arm_level.txt',
                    'class': 'File',
                    'checksum': 'sha1$9f89c90a0f196ab2771f5e9aadc5893a5e509609',
                    'size': 2148,
                    'path': os.path.join(output_dir, 'Sample24.Sample23.arm_level.txt')
                    },
                'gene_level_txt': {
                    'location': 'file://' + os.path.join(output_dir, 'Sample24.Sample23.gene_level.txt'),
                    'basename': 'Sample24.Sample23.gene_level.txt',
                    'class': 'File',
                    'checksum': 'sha1$f056daac29597163fecb90e69d801953a74c7619',
                    'size': 156007,
                    'path': os.path.join(output_dir, 'Sample24.Sample23.gene_level.txt')
                },
                'hisens_rds': {
                    'location': 'file://' + os.path.join(output_dir, 'Sample24.Sample23_hisens.rds'),
                    'basename': 'Sample24.Sample23_hisens.rds',
                    'class': 'File',
                    'checksum': 'sha1$6bfd6c7f29c49ec8ef538dd468a3b4626b05bda2',
                    'size': 213986,
                    'path': os.path.join(output_dir, 'Sample24.Sample23_hisens.rds')
                },
                'hisens_seg': {
                    'location': 'file://' + os.path.join(output_dir, 'Sample24.Sample23_hisens.seg'),
                    'basename': 'Sample24.Sample23_hisens.seg',
                    'class': 'File',
                    'checksum': 'sha1$1ddb1a4a43c5707188ae597792c372eee2910d1c',
                    'size': 2221,
                    'path': os.path.join(output_dir, 'Sample24.Sample23_hisens.seg')
                },
                'output_txt': {
                    'location': 'file://' + os.path.join(output_dir, 'Sample24.Sample23.txt'),
                    'basename': 'Sample24.Sample23.txt',
                    'class': 'File',
                    'checksum': 'sha1$b1cc75293a4bddfe36540a6ea4248a44acae6db0',
                    'size': 498,
                    'path': os.path.join(output_dir, 'Sample24.Sample23.txt')
                },
                'purity_rds': {
                    'location': 'file://' + os.path.join(output_dir, 'Sample24.Sample23_purity.rds'),
                    'basename': 'Sample24.Sample23_purity.rds',
                    'class': 'File',
                    'checksum': 'sha1$dd8b967f84b191ff76214c6110db8d0e65f6514c',
                    'size': 213356,
                    'path': os.path.join(output_dir, 'Sample24.Sample23_purity.rds')
                },
                'purity_seg': {
                    'location': 'file://' + os.path.join(output_dir, 'Sample24.Sample23_purity.seg'),
                    'basename': 'Sample24.Sample23_purity.seg',
                    'class': 'File',
                    'checksum': 'sha1$dadb691707754772520a82c9148620d428281328',
                    'size': 1501,
                    'path': os.path.join(output_dir, 'Sample24.Sample23_purity.seg')
                },
                'qc_txt': {
                    'location': 'file://' + os.path.join(output_dir, 'Sample24.Sample23.qc.txt'),
                    'basename': 'Sample24.Sample23.qc.txt',
                    'class': 'File',
                    'checksum': 'sha1$704180fe9d6ccf38a7332d40b524bea3a2d3ff98',
                    'size': 1357,
                    'path': os.path.join(output_dir, 'Sample24.Sample23.qc.txt')
                }
            }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

if __name__ == "__main__":
    unittest.main()
