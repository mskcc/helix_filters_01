#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the replace.cwl file
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

cwl_file = os.path.join(CWL_DIR, 'replace.cwl')

class TestReplace(unittest.TestCase):
    def test_replace1(self):
        """
        Test that strings get replaced
        """
        with TemporaryDirectory() as tmpdir:
            # make a dummy file with some lines
            input_lines = ["HEADER", "foo", "ILLOGICAL", "baz"]
            input_file = os.path.join(tmpdir, "input.txt")
            with open(input_file, "w") as fout:
                for line in input_lines:
                    fout.write(line + '\n')

            input_json = {
                "input_file":{
                      "class": "File",
                      "path": input_file
                    },
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

            # check the contents of the concatenated file; should be the same as the input
            output_file = output_json['output_file']['path']
            with open(output_file) as fin:
                output_lines = [ line.strip() for line in fin ]

            expected_lines = ["HEADER", "foo", "NA", "baz"]
            self.assertEqual(output_lines, expected_lines)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$62255c8ee13b8ba6e01c7e17262a8ba1f174e5cb',
                    'size': 18,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)


if __name__ == "__main__":
    unittest.main()
