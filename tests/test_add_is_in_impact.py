#!/usr/bin/env python3
"""
unit tests for the add_is_in_impact.py script
"""
import os
import unittest
from tempfile import TemporaryDirectory

# relative imports, from CLI and from parent project
if __name__ != "__main__":
    from .tools import run_command, load_mutations
    from .settings import DATA_SETS, BIN_DIR

if __name__ == "__main__":
    from tools import run_command, load_mutations
    from settings import DATA_SETS, BIN_DIR

impact_script = os.path.join(BIN_DIR, 'add_is_in_impact.py')

def create_sample_maf(tmpdir, filename = "input.maf"):
    filepath = os.path.join(tmpdir, filename)
    lines = [
    ['Chromosome', 'Start_Position'],
    ['1', '100'],
    ['2', '200'],
    ['3', '300'],
    ['4', '400']
    ]
    with open(filepath, "w") as f:
        for line in lines:
            line_str = '\t'.join(line) + '\n'
            f.write(line_str)
    return(filepath)

def create_impact_file(tmpdir, filename = "IMAPCT.txt"):
    filepath = os.path.join(tmpdir, filename)
    lines = [
    ['1', '50', '150'] # chrom, start, stop
    ]
    with open(filepath, "w") as f:
        for line in lines:
            line_str = '\t'.join(line) + '\n'
            f.write(line_str)
    return(filepath)

class TestInImpactScript(unittest.TestCase):
    def test_is_in_impact1(self):
        """
        """
        # run the script in a temporary directory
        with TemporaryDirectory() as tmpdir:
            input_maf_file = create_sample_maf(tmpdir = tmpdir)
            impact_file = create_impact_file(tmpdir = tmpdir)
            output_file = os.path.join(tmpdir, "output.txt")

            # command line arguments to run script
            command = [ impact_script, '--input_file', input_maf_file, '--output_file', output_file, '--IMPACT_file', impact_file ]
            returncode, proc_stdout, proc_stderr = run_command(command)

            # check that it ran successfully
            if returncode != 0:
                print(proc_stderr)

            self.assertEqual(returncode, 0)

# run the test suite from the command line
if __name__ == "__main__":
    unittest.main()
