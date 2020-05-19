#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
unit tests for the concat.cwl
"""
import os
import json
import unittest
from tempfile import TemporaryDirectory, NamedTemporaryFile

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command
    from .settings import CWL_DIR, CWL_ARGS

if __name__ == "__main__":
    from tools import run_command
    from settings import CWL_DIR, CWL_ARGS

cwl_file = os.path.join(CWL_DIR, 'concat.cwl')

class TestMafFilter(unittest.TestCase):
    def test_concat_simple_file(self):
        """
        Test that a single file with no header comes out looking as expected
        """
        with TemporaryDirectory() as tmpdir:

            # make a dummy file with some lines
            input_lines = ["foo", "bar", "baz"]
            input_file = os.path.join(tmpdir, "input.txt")
            with open(input_file, "w") as fout:
                for line in input_lines:
                    fout.write(line + '\n')

            input_json = {
                "input_files": [{
                      "class": "File",
                      "path": input_file
                    }]
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

            # check the contents of the concatenated file; should be the same as the input
            output_file = output_json['output_file']['path']
            with open(output_file) as fin:
                output_lines = [ line.strip() for line in fin ]

            self.assertEqual(output_lines, input_lines)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$0562f08aef399135936d6fb4eb0cc7bc1890d5b4',
                    'size': 12,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)

    def test_concat_simple_file_with_header(self):
        """
        Test that a single file with no header comes out looking as expected
        """
        with TemporaryDirectory() as tmpdir:

            # make a dummy file with some lines
            input_lines = ["#header", "foo", "bar", "baz"]
            input_file = os.path.join(tmpdir, "input.txt")
            with open(input_file, "w") as fout:
                for line in input_lines:
                    fout.write(line + '\n')

            input_json = {
                "input_files": [{
                      "class": "File",
                      "path": input_file
                    }]
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

            # check the contents of the concatenated file; should be the same as the input
            output_file = output_json['output_file']['path']
            with open(output_file) as fin:
                output_lines = [ line.strip() for line in fin ]

            self.assertEqual(output_lines, ["foo", "bar", "baz"])

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$0562f08aef399135936d6fb4eb0cc7bc1890d5b4',
                    'size': 12,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)

    def test_concat_two_files_with_headers(self):
        """
        Test that a single file with no header comes out looking as expected
        """
        with TemporaryDirectory() as tmpdir:

            # make a dummy file with some lines
            input_lines1 = ["#header1", "foo1", "bar1", "baz1"]
            input_file1 = os.path.join(tmpdir, "input1.txt")
            with open(input_file1, "w") as fout:
                for line in input_lines1:
                    fout.write(line + '\n')

            input_lines2 = ["#header2", "foo2", "bar2", "baz2"]
            input_file2 = os.path.join(tmpdir, "input1.txt")
            with open(input_file2, "w") as fout:
                for line in input_lines2:
                    fout.write(line + '\n')

            input_json = {
                "input_files": [
                    {
                      "class": "File",
                      "path": input_file1
                    },
                    {
                      "class": "File",
                      "path": input_file2
                    }
                    ]
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

            # check the contents of the concatenated file; should be the same as the input
            output_file = output_json['output_file']['path']
            with open(output_file) as fin:
                output_lines = [ line.strip() for line in fin ]

            self.assertEqual(output_lines, ["foo1", "bar1", "baz1", "foo2", "bar2", "baz2"])

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$0562f08aef399135936d6fb4eb0cc7bc1890d5b4',
                    'size': 12,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)




if __name__ == "__main__":
    unittest.main()
