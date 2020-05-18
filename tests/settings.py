import os
THIS_DIR = os.path.dirname(os.path.abspath(__file__))

CWL_DIR = os.path.join(os.path.dirname(THIS_DIR), "cwl")
CWL_ARGS = ["--preserve-environment", "PATH", "--preserve-environment", "SINGULARITY_CACHEDIR"]
