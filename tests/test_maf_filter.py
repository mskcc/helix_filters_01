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
    from .settings import CWL_DIR, CWL_ARGS, DATA_SETS, ARGOS_VERSION_STRING, IS_IMPACT

if __name__ == "__main__":
    from tools import run_command
    from settings import CWL_DIR, CWL_ARGS, DATA_SETS, ARGOS_VERSION_STRING, IS_IMPACT

cwl_file = os.path.join(CWL_DIR, 'maf_filter.cwl')

class TestMafFilter(unittest.TestCase):
    def test_filter_a_maf_file(self):
        """
        Test that a filtered maf file comes out as expected
        """
        input_maf = os.path.join(DATA_SETS['Proj_08390_G']['MAF_DIR'], "Sample1.Sample2.muts.maf")

        with open(input_maf) as fin:
            input_maf_lines = len(fin.readlines())

        self.assertEqual(input_maf_lines, 12518)

        with TemporaryDirectory() as tmpdir:
            output_dir = os.path.join(tmpdir, "output")
            input_json = {
                "maf_file": {
                      "class": "File",
                      "path": input_maf
                    },
                "argos_version_string": ARGOS_VERSION_STRING,
                "is_impact": IS_IMPACT,
                "analysis_mutations_filename": "Proj_08390_G.muts.maf",
                "cbio_mutation_data_filename": 'data_mutations_extended.txt'
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

            with open(output_json['analysis_mutations_file']['path']) as fin:
                output_maf_lines = len(fin.readlines())
            self.assertEqual(output_maf_lines, 24)

            expected_output = {
                'analysis_mutations_file': {
                    'location': 'file://' + os.path.join(output_dir, "Proj_08390_G.muts.maf"),
                    'basename': "Proj_08390_G.muts.maf",
                    'class': 'File',
                    'checksum': 'sha1$49086adcecc296905ed210ce512bf71a56a4e71a',
                    'size': 27917,
                    'path': os.path.join(output_dir, "Proj_08390_G.muts.maf")
                    },
                'cbio_mutation_data_file': {
                    'location': 'file://' + os.path.join(output_dir, 'data_mutations_extended.txt'),
                    'basename': 'data_mutations_extended.txt',
                    'class': 'File',
                    'checksum': 'sha1$f35288b7d321e34f17abbcb02e29df942e308601',
                    'size': 4372,
                    'path': os.path.join(output_dir, 'data_mutations_extended.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)

    def test_maf_filter_argos_3_2_0(self):
        """
        Test the maf filter script results when used with argos_version_string 3.2.0
        """
        input_maf = os.path.join(DATA_SETS['Proj_08390_G']['MAF_DIR'], "Sample1.Sample2.muts.maf")

        with open(input_maf) as fin:
            input_maf_lines = len(fin.readlines())

        self.assertEqual(input_maf_lines, 12518)

        with TemporaryDirectory() as tmpdir:
            output_dir = os.path.join(tmpdir, "output")
            input_json = {
                "maf_file": {
                      "class": "File",
                      "path": input_maf
                    },
                "argos_version_string": "3.2.0",
                "is_impact": IS_IMPACT,
                "analysis_mutations_filename": "Proj_08390_G.muts.maf",
                "cbio_mutation_data_filename": 'data_mutations_extended.txt'
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
                'analysis_mutations_file': {
                    'location': 'file://' + os.path.join(output_dir, "Proj_08390_G.muts.maf"),
                    'basename': "Proj_08390_G.muts.maf",
                    'class': 'File',
                    'checksum': 'sha1$d9e2e80b925857252097c28d37e1aa0d879058c4',
                    'size': 27919,
                    'path': os.path.join(output_dir, "Proj_08390_G.muts.maf")
                    },
                'cbio_mutation_data_file': {
                    'location': 'file://' + os.path.join(output_dir, 'data_mutations_extended.txt'),
                    'basename': 'data_mutations_extended.txt',
                    'class': 'File',
                    'checksum': 'sha1$7f34d57cf40cec8ce8e0d9d5306380e5abfb4b70',
                    'size': 4374,
                    'path': os.path.join(output_dir, 'data_mutations_extended.txt')
                    }
                }

            with open(output_json['analysis_mutations_file']['path']) as fin:
                output_maf_lines = len(fin.readlines())
            self.assertEqual(output_maf_lines, 24)

            self.assertDictEqual(output_json, expected_output)

    def test_filter_maf_file_impact_false(self):
        """
        Test that a filtered maf file comes out as expected
        """
        input_maf = os.path.join(DATA_SETS['Proj_08390_G']['MAF_DIR'], "Sample1.Sample2.muts.maf")

        with open(input_maf) as fin:
            input_maf_lines = len(fin.readlines())

        self.assertEqual(input_maf_lines, 12518)

        with TemporaryDirectory() as tmpdir:
            output_dir = os.path.join(tmpdir, "output")
            input_json = {
                "maf_file": {
                      "class": "File",
                      "path": input_maf
                    },
                "argos_version_string": ARGOS_VERSION_STRING,
                "is_impact": "False",
                "analysis_mutations_filename": "Proj_08390_G.muts.maf",
                "cbio_mutation_data_filename": 'data_mutations_extended.txt'
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

            with open(output_json['analysis_mutations_file']['path']) as fin:
                output_maf_lines = len(fin.readlines())
            self.assertEqual(output_maf_lines, 20)

            expected_output = {
                'analysis_mutations_file': {
                    'location': 'file://' + os.path.join(output_dir, "Proj_08390_G.muts.maf"),
                    'basename': "Proj_08390_G.muts.maf",
                    'class': 'File',
                    'checksum': 'sha1$1f9ad9aec62836740f39732ea193591a725891f6',
                    'size': 24362,
                    'path': os.path.join(output_dir, "Proj_08390_G.muts.maf")
                    },
                'cbio_mutation_data_file': {
                    'location': 'file://' + os.path.join(output_dir, 'data_mutations_extended.txt'),
                    'basename': 'data_mutations_extended.txt',
                    'class': 'File',
                    'checksum': 'sha1$93fa92e4da62c072dbe8f0aa2d5ca733f3d44213',
                    'size': 3769,
                    'path': os.path.join(output_dir, 'data_mutations_extended.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)


if __name__ == "__main__":
    unittest.main()
