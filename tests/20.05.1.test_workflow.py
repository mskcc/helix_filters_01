#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for the workflow.cwl
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

cwl_file = os.path.join(CWL_DIR, 'workflow.cwl')

class TestWorkflow(unittest.TestCase):
    def test_run_worflow_one_maf(self):
        """
        Test that the workflow works correctly when run with a single maf
        """
        input_json = {
            "analyst_file": "Proj_08390_G.muts.maf",
            "is_impact": IS_IMPACT,
            "portal_file": PORTAL_FILE,
            "argos_version_string": ARGOS_VERSION_STRING,
            "portal_CNA_file": PORTAL_CNA_FILE,
            "maf_files": [
                {
                    "path": os.path.join(DATA_SETS['Proj_08390_G']['DIR'], "maf/Sample1.Sample2.muts.maf"),
                    "class": "File"
                }
            ],
            "hisens_cncfs": [
                {
                    "path": os.path.join(DATA_SETS['Proj_08390_G']['DIR'], "facets/Sample2.rg.md.abra.printreads__Sample1.rg.md.abra.printreads_hisens.cncf.txt"),
                    "class": "File"
                },
                {
                    "path": os.path.join(DATA_SETS['Proj_08390_G']['DIR'], "facets/Sample3.rg.md.abra.printreads__Sample4.rg.md.abra.printreads_hisens.cncf.txt"),
                    "class": "File"
                }
            ],
            "analysis_gene_cna_file": "Proj_08390_G.gene.cna.txt",
            "targets_list": {
                "path": "/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist",
                "class": "File"
            }
        }

        with TemporaryDirectory() as tmpdir:

            input_json_file = os.path.join(tmpdir, "input.json")
            with open(input_json_file, "w") as json_out:
                json.dump(input_json, json_out)
            # input_json_file = os.path.join(DATA_SETS['Proj_08390_G']['DIR'], "input.one_maf.2.json")

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
            # print(returncode, proc_stdout, proc_stderr, output_json)

            expected_output = {
                'analysis_gene_cna_file': {
                    'location': 'file://' + os.path.join(output_dir, 'Proj_08390_G.gene.cna.txt'),
                    'basename': 'Proj_08390_G.gene.cna.txt',
                    'class': 'File',
                    'checksum': 'sha1$ab17d587ad5ae0a87fd6c6d4dd2d5d1701208ce9',
                    'size': 173982,
                    'path': os.path.join(output_dir, 'Proj_08390_G.gene.cna.txt')
                    },
                'analyst_file': {
                    'location': 'file://' + os.path.join(output_dir, 'Proj_08390_G.muts.maf'),
                    'basename': 'Proj_08390_G.muts.maf',
                    'class': 'File',
                    'checksum': 'sha1$7a1dbde2f538e72d1dcb9baa7def46922e7454d9',
                    'size': 27901,
                    'path': os.path.join(output_dir, 'Proj_08390_G.muts.maf')
                    },
                'output_portal_CNA_file': {
                    'location': 'file://' + os.path.join(output_dir, 'data_CNA.txt'),
                    'basename': 'data_CNA.txt',
                    'class': 'File',
                    'checksum': 'sha1$ab17d587ad5ae0a87fd6c6d4dd2d5d1701208ce9',
                    'size': 173982,
                    'path': os.path.join(output_dir, 'data_CNA.txt')
                    }
                }

            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

    def test_run_worflow_two_mafs(self):
        """
        Test that the workflow works correctly when run with a
        """
        input_json = {
            "analyst_file": "Proj_08390_G.muts.maf",
            "is_impact": IS_IMPACT,
            "portal_file": PORTAL_FILE,
            "argos_version_string": ARGOS_VERSION_STRING,
            "portal_CNA_file": PORTAL_CNA_FILE,
            "maf_files": [
                {
                    "path": os.path.join(DATA_SETS['Proj_08390_G']['DIR'], "maf/Sample1.Sample2.muts.maf"),
                    "class": "File"
                },
                {
                    "path": os.path.join(DATA_SETS['Proj_08390_G']['DIR'], "maf/Sample4.Sample3.muts.maf"),
                    "class": "File"
                }
            ],
            "hisens_cncfs": [
                {
                    "path": os.path.join(DATA_SETS['Proj_08390_G']['DIR'], "facets/Sample2.rg.md.abra.printreads__Sample1.rg.md.abra.printreads_hisens.cncf.txt"),
                    "class": "File"
                },
                {
                    "path": os.path.join(DATA_SETS['Proj_08390_G']['DIR'], "facets/Sample3.rg.md.abra.printreads__Sample4.rg.md.abra.printreads_hisens.cncf.txt"),
                    "class": "File"
                }
            ],
            "analysis_gene_cna_file": "Proj_08390_G.gene.cna.txt",
            "targets_list": {
                "path": "/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist",
                "class": "File"
            }
        }
        with TemporaryDirectory() as tmpdir:
            # input_json_file = os.path.join(DATA_SETS['Proj_08390_G']['DIR'], "input.all.json")
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
            # print(returncode, proc_stdout, proc_stderr, output_json)

            expected_output = {
                'analysis_gene_cna_file': {
                    'location': 'file://' + os.path.join(output_dir, 'Proj_08390_G.gene.cna.txt'),
                    'basename': 'Proj_08390_G.gene.cna.txt',
                    'class': 'File',
                    'checksum': 'sha1$ab17d587ad5ae0a87fd6c6d4dd2d5d1701208ce9',
                    'size': 173982,
                    'path': os.path.join(output_dir, 'Proj_08390_G.gene.cna.txt')
                    },
                'analyst_file': {
                    'location': 'file://' + os.path.join(output_dir, 'Proj_08390_G.muts.maf'),
                    'basename': 'Proj_08390_G.muts.maf',
                    'class': 'File',
                    'checksum': 'sha1$5b2f8277269026d2b7ea0edc4455cc97c7f68523',
                    'size': 46695,
                    'path': os.path.join(output_dir, 'Proj_08390_G.muts.maf')
                    },
                'output_portal_CNA_file': {
                    'location': 'file://' + os.path.join(output_dir, 'data_CNA.txt'),
                    'basename': 'data_CNA.txt',
                    'class': 'File',
                    'checksum': 'sha1$ab17d587ad5ae0a87fd6c6d4dd2d5d1701208ce9',
                    'size': 173982,
                    'path': os.path.join(output_dir, 'data_CNA.txt')
                    }
                }

            self.maxDiff = None
            self.assertDictEqual(output_json, expected_output)

if __name__ == "__main__":
    unittest.main()
