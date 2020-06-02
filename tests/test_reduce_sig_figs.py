#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for reduce_sig_figs.cwl
"""
import os
import json
import csv
import unittest
from collections import OrderedDict
from tempfile import TemporaryDirectory

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command
    from .settings import CWL_DIR, CWL_ARGS

if __name__ == "__main__":
    from tools import run_command
    from settings import CWL_DIR, CWL_ARGS

cwl_file = os.path.join(CWL_DIR, 'reduce_sig_figs.cwl')

class TestReduceSigFigs(unittest.TestCase):
    def test_reduce_sig_figs(self):
        """
        Test that significant figures are reduced correctly
        """

        with TemporaryDirectory() as tmpdir:

            # make a dummy file with some lines
            input_lines = ["seg.mean", "3.141592", "2.718281828"]
            input_file = os.path.join(tmpdir, "input.txt")
            with open(input_file, "w") as fout:
                for line in input_lines:
                    fout.write(line + '\n')

            input_json = {
                "input_file": {
                      "class": "File",
                      "path": input_file
                    }
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

            # check the contents of the file
            output_file = output_json['output_file']['path']
            with open(output_file) as fin:
                reader = csv.DictReader(fin)
                rows = [ row for row in reader ]

            self.assertEqual(len(rows), 2)
            self.assertDictEqual(rows[0], OrderedDict([('seg.mean', '3.1416')]))
            self.assertDictEqual(rows[1], OrderedDict([('seg.mean', '2.7183')]))


            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$d9f5ec4a9aa27a69ee64edb97eb10d6db65c7ad7',
                    'size': 26,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)




if __name__ == "__main__":
    unittest.main()
