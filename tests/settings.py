"""
Put settings to use for the tests in here for easier access
"""
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CWL_DIR = os.path.join(os.path.dirname(THIS_DIR), "cwl")

# common args to be included in all cwltool invocations
CWL_ARGS = [
    "--preserve-environment", "PATH",
    "--preserve-environment", "SINGULARITY_CACHEDIR",
    "--singularity"
]

# location on the filesystem for static fixtures
FIXTURES_DIR = '/juno/work/ci/helix_filters_01/fixtures'

DATA_SETS = {
    "Proj_08390_G": {
        "DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G"),
        "MAF_DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G", "maf"),
        "FACETS_DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G", "facets"),
        "INPUTS_DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G", "inputs"),
        "targets_list": "/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist",
        "argos_version_string": "2.x",
        "is_impact": True,
        "analyst_file": "Proj_08390_G.muts.maf",
        "analysis_gene_cna_file": "Proj_08390_G.gene.cna.txt",
        "portal_file": "data_mutations_extended.txt",
        "portal_CNA_file": "data_CNA.txt",
    }
}
