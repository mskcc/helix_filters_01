"""
Put settings to use for the tests in here for easier access
"""
import os

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
CWL_DIR = os.path.join(os.path.dirname(THIS_DIR), "cwl")
REF_DIR = os.path.join(os.path.dirname(THIS_DIR), "ref")

# common args to be included in all cwltool invocations
CWL_ARGS = [
    "--preserve-environment", "PATH",
    "--preserve-environment", "SINGULARITY_CACHEDIR",
    "--singularity"
]

# location on the filesystem for static fixtures
FIXTURES_DIR = os.environ.get('FIXTURES_DIR', '/juno/work/ci/helix_filters_01/fixtures')

KNOWN_FUSIONS_FILE = os.path.join(REF_DIR, "known_fusions_at_mskcc.txt")

ARGOS_VERSION_STRING = os.environ.get('ARGOS_VERSION_STRING', '2.x') # TODO: deprecate this
IS_IMPACT = os.environ.get('IS_IMPACT', "True") # TODO: deprecate this
PORTAL_FILE = os.environ.get('PORTAL_FILE', 'data_mutations_extended.txt') # TODO: deprecate this
PORTAL_CNA_FILE = os.environ.get('PORTAL_CNA_FILE', 'data_CNA.txt') # TODO: deprecate this


DATA_SETS = {
    "Proj_08390_G": {
        "DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G"),
        "MAF_DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G", "maf"),
        "FACETS_DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G", "facets"),
        "INPUTS_DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G", "inputs"),
        "QC_DIR": os.path.join(FIXTURES_DIR, "Proj_08390_G", "qc"),
        "targets_list": "/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist",
        "analyst_file": "Proj_08390_G.muts.maf", # TODO: deprecate this
        "analysis_gene_cna_file": "Proj_08390_G.gene.cna.txt", # TODO: deprecate this
    }
}
