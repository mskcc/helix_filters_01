#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for the facets-workflow.cwl
"""
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile


# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command
    from .settings import CWL_DIR, CWL_ARGS, DATA_SETS, FACETS_SNPS_VCF

if __name__ == "__main__":
    from tools import run_command
    from settings import CWL_DIR, CWL_ARGS, DATA_SETS, FACETS_SNPS_VCF

cwl_file = os.path.join(CWL_DIR, 'facets-workflow.cwl')

class TestFacetsWorkflow(unittest.TestCase):
    def test_facets_workflow(self):
        """
        """
        # the smallest pair of bam files in the test dataset
        tumor_bam = os.path.join(DATA_SETS['Proj_08390_G']['BAM_DIR'], "Sample24.rg.md.abra.printreads.bam")
        normal_bam = os.path.join(DATA_SETS['Proj_08390_G']['BAM_DIR'], "Sample23.rg.md.abra.printreads.bam")
        pair_maf = os.path.join(DATA_SETS['Proj_08390_G']['MAF_DIR'], "Sample24.Sample23.muts.maf")
        input_json = {
            "snps_vcf": {
                "path": FACETS_SNPS_VCF,
                "class": "File"
            },
            "pairs": [
                {
                    "normal_bam": {
                        "path": normal_bam,
                        "class": "File"
                    },
                    "tumor_bam": {
                        "path": tumor_bam,
                        "class": "File"
                    },
                    "pair_maf": {
                        "path": pair_maf,
                        "class": "File"
                    },
                    "pair_id": "Sample24.Sample23"
                }
            ]
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
            print(output_json)
            self.maxDiff = None
            self.assertDictEqual(output_json, {})

if __name__ == "__main__":
    unittest.main()
