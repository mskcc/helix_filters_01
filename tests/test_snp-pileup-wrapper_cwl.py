#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the snp-pileup-wrapper.cwl file
"""
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile


# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command
    from .settings import CWL_DIR, CWL_ARGS, FACETS_SNPS_VCF, DATA_SETS

if __name__ == "__main__":
    from tools import run_command
    from settings import CWL_DIR, CWL_ARGS, FACETS_SNPS_VCF, DATA_SETS

cwl_file = os.path.join(CWL_DIR, 'snp-pileup-wrapper.cwl')

class TestSnpPileupCWL(unittest.TestCase):
    def test_snp_pileup1(self):
        """
        """
        input_json = {
            "snps_vcf": {
                "path": FACETS_SNPS_VCF,
                "class": "File"
            },
            # the smallest pair of bam files in the test dataset
            "normal_bam": {
                "path": os.path.join(DATA_SETS['Proj_08390_G']['BAM_DIR'], "Sample23.rg.md.abra.printreads.bam"),
                "class": "File"
            },
            "tumor_bam": {
                "path": os.path.join(DATA_SETS['Proj_08390_G']['BAM_DIR'], "Sample24.rg.md.abra.printreads.bam"),
                "class": "File"
            },
            "output_prefix": "Sample24.Sample23"
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
                    'location': 'file://' + os.path.join(output_dir, "Sample24.Sample23.snp_pileup.gz"),
                    'basename': "Sample24.Sample23.snp_pileup.gz",
                    'class': 'File',
                    'checksum': 'sha1$755a8b64f45c819b4e2c481e64bf2fe36d1f5361',
                    'size': 34851004,
                    'path': os.path.join(output_dir, "Sample24.Sample23.snp_pileup.gz")
                    }
                }
            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

if __name__ == "__main__":
    unittest.main()
