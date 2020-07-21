#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
unit tests for the tools module
"""
import os
import unittest
from tempfile import TemporaryDirectory

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import md5

if __name__ == "__main__":
    from tools import md5

class TestTools(unittest.TestCase):
    def test_md5(self):
        with TemporaryDirectory() as tmpdir:
            filename = os.path.join(tmpdir, "file.txt")
            lines = ['foo', 'bar']
            with open(filename, "w") as fout:
                for line in lines:
                    fout.write(line + '\n')
            hash = md5(filename)
            self.assertEqual(hash, 'f47c75614087a8dd938ba4acff252494')

if __name__ == "__main__":
    unittest.main()
