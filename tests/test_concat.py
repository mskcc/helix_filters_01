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

class TestConcat(unittest.TestCase):
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
            input_lines1 = ["header","foo1", "bar1", "baz1"]
            input_file1 = os.path.join(tmpdir, "input1.txt")
            with open(input_file1, "w") as fout:
                for line in input_lines1:
                    fout.write(line + '\n')

            input_lines2 = ["header","foo2", "bar2", "baz2"]
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
                    }
                    ]
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

            self.assertEqual(output_lines, ["header","foo1", "bar1", "baz1", "foo2", "bar2", "baz2"])

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$34c3af14e6d21e295f22c77ed5e837b60501bae7',
                    'size': 37,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)

    def test_concat_two_files_with_comments(self):
        """
        Test that a two files with headers are concatenated correctly
        """
        with TemporaryDirectory() as tmpdir:

            # make a dummy file with some lines
            input_lines1 = ["#comment1", "header1", "foo1", "bar1", "baz1"]
            input_file1 = os.path.join(tmpdir, "input1.txt")
            with open(input_file1, "w") as fout:
                for line in input_lines1:
                    fout.write(line + '\n')

            input_lines2 = ["#comment2", "header2", "foo2", "bar2", "baz2"]
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
                    }
                    ]
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

            self.assertEqual(output_lines, ["header1", "foo1", "bar1", "baz1", "foo2", "bar2", "baz2"])

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$acaa1f09ca0678b8b7c136ce776c04efb6890f6a',
                    'size': 38,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)

    def test_concat_two_mixed_files(self):
        """
        Test that two files, one with a comment and one without, are concatenated correctly
        """
        with TemporaryDirectory() as tmpdir:

            # make a dummy file with some lines
            input_lines1 = ["header1", "foo1", "bar1", "baz1"]
            input_file1 = os.path.join(tmpdir, "input1.txt")
            with open(input_file1, "w") as fout:
                for line in input_lines1:
                    fout.write(line + '\n')

            input_lines2 = ["#comment2", "header2", "foo2", "bar2", "baz2"]
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
                    }
                    ]
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

            self.assertEqual(output_lines, ["header1", "foo1", "bar1", "baz1", "foo2", "bar2", "baz2"])

            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$acaa1f09ca0678b8b7c136ce776c04efb6890f6a',
                    'size': 38,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)

    def test_concat_three_files_with_comments(self):
        """
        Test that a three files with headers are concatenated correctly
        Use three this time to clearly show the ordering of the output iteration
        """
        with TemporaryDirectory() as tmpdir:

            # make a dummy file with some lines
            input_lines1 = ["#comment1", "header1", "foo1", "bar1", "baz1"]
            input_file1 = os.path.join(tmpdir, "input1.txt")
            with open(input_file1, "w") as fout:
                for line in input_lines1:
                    fout.write(line + '\n')

            input_lines2 = ["#comment2", "header2", "foo2", "bar2", "baz2"]
            input_file2 = os.path.join(tmpdir, "input2.txt")
            with open(input_file2, "w") as fout:
                for line in input_lines2:
                    fout.write(line + '\n')

            input_lines3 = ["#comment3", "header3", "foo3", "bar3", "baz3"]
            input_file3 = os.path.join(tmpdir, "input3.txt")
            with open(input_file3, "w") as fout:
                for line in input_lines3:
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
                    {
                      "class": "File",
                      "path": input_file3
                    }
                    ]
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

            expected_output_lines = ["header1", "foo1", "bar1", "baz1", "foo2", "bar2", "baz2", "foo3", "bar3", "baz3"]
            self.assertEqual(output_lines, expected_output_lines)

            # TODO: update this once the above ^^^ passes
            expected_output = {
                'output_file': {
                    'location': 'file://' + os.path.join(output_dir, 'output.txt'),
                    'basename': 'output.txt',
                    'class': 'File',
                    'checksum': 'sha1$b115b7b40aa8a2e08e30a55abf60d742e05e62b4',
                    'size': 53,
                    'path': os.path.join(output_dir, 'output.txt')
                    }
                }
            self.assertDictEqual(output_json, expected_output)




if __name__ == "__main__":
    unittest.main()
