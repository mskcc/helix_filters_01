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
    from .settings import CWL_DIR, CWL_ARGS

if __name__ == "__main__":
    from tools import run_command
    from settings import CWL_DIR, CWL_ARGS

cwl_file = os.path.join(CWL_DIR, 'concat_with_comments.cwl')

class TestConcatWithCommentsCWL(unittest.TestCase):
    def test_concat_0(self):
        """
        Test concat when no comments are present in the original file
        """
        with TemporaryDirectory() as tmpdir:
            # make a dummy file with some lines
            input_lines = ["HEADER", "foo", "bar", "baz"]
            input_file = os.path.join(tmpdir, "input.txt")
            with open(input_file, "w") as fout:
                for line in input_lines:
                    fout.write(line + '\n')

            input_json = {
                "input_files": [{
                      "class": "File",
                      "path": input_file
                    }],
                "comment_label": "comment_label",
                "comment_value": "comment_value"
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

            expected_lines = ['#comment_label: comment_value', "HEADER", 'foo', 'bar', 'baz']
            self.assertEqual(output_lines, expected_lines)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$7cef8f6de47289a55de99de77563beb3fa371deb',
                    'size': 49,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)

    def test_concat1(self):
        """
        Test concat when original file has a comment line
        """
        with TemporaryDirectory() as tmpdir:
            # make a dummy file with some lines
            input_lines = ["# comment here", "HEADER", "foo", "bar", "baz"]
            input_file = os.path.join(tmpdir, "input.txt")
            with open(input_file, "w") as fout:
                for line in input_lines:
                    fout.write(line + '\n')

            input_json = {
                "input_files": [{
                      "class": "File",
                      "path": input_file
                    }],
                "comment_label": "comment_label",
                "comment_value": "comment_value"
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

            expected_lines = ['# comment here', '#comment_label: comment_value', "HEADER", 'foo', 'bar', 'baz']
            self.assertEqual(output_lines, expected_lines)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$14ee1247f314dba1e3c28aa8aec9ff7b137a1f41',
                    'size': 64,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)

    def test_concat2(self):
        """
        Test concat when multiple files have comments
        """
        with TemporaryDirectory() as tmpdir:
            # make a dummy file with some lines
            input_lines1 = ["# comment 1 here", "HEADER", "foo1", "bar1"]
            input_file1 = os.path.join(tmpdir, "input1.txt")
            with open(input_file1, "w") as fout:
                for line in input_lines1:
                    fout.write(line + '\n')

            input_lines2 = ["# comment 2 here", "HEADER", "foo2", "bar2"]
            input_file2 = os.path.join(tmpdir, "input2.txt")
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
                    },
                    ],
                "comment_label": "comment_label",
                "comment_value": "comment_value"
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

            expected_lines = [
                '# comment 1 here',
                '# comment 2 here',
                '#comment_label: comment_value',
                "HEADER",
                'foo1',
                'bar1',
                'foo2',
                'bar2'
                ]
            self.maxDiff = None
            self.assertEqual(output_lines, expected_lines)

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$5dbce16f9bfef135d6b8288b16350351a33998f3',
                    'size': 91,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)


if __name__ == "__main__":
    unittest.main()
