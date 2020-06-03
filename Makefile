export SHELL:=/bin/bash
.ONESHELL:
export SHELLOPTS:=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit

define help
This is the Makefile for helix filters

This repo contains scripts and workflows for usage with the Roslin pipeline in order to filter variant calling results

The subdir "roslin-post" is meant to include the main helix filter workflow + extra cBio Portal file generations (in development)

Dependencies can be installed with:

make install

Example usage of this helix filter workflow:

make run PROJ_ID=My_Project MAF_DIR=/path/to/outputs/maf FACETS_DIR=/path/to/outputs/facets OUTPUT_DIR=/path/to/helix_filters TARGETS_LIST=/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist

check the file 'ref/roslin_resources.json' to find the correct target set for your assay type

Run the test suite:

make test

NOTE: requires the fixtures directory on juno

endef
export help
help:
	@printf "$$help"
.PHONY : help

UNAME:=$(shell uname)
export SINGULARITY_CACHEDIR:=/juno/work/ci/singularity_images
export PATH:=$(CURDIR)/conda/bin:$(CURDIR)/bin:$(PATH)
unexport PYTHONPATH
unexport PYTHONHOME

ifeq ($(UNAME), Darwin)
CONDASH:=Miniconda3-4.5.4-MacOSX-x86_64.sh
endif

ifeq ($(UNAME), Linux)
CONDASH:=Miniconda3-4.5.4-Linux-x86_64.sh
endif

CONDAURL:=https://repo.continuum.io/miniconda/$(CONDASH)

conda:
	@echo ">>> Setting up conda..."
	@wget "$(CONDAURL)" && \
	bash "$(CONDASH)" -b -p conda && \
	rm -f "$(CONDASH)"

install: conda
	conda install -y \
	conda-forge::jq=1.5
	pip install \
	cwltool==2.0.20200126090152 \
	cwlref-runner==1.0

# example values; set these from the command line for real-world usage
export PROJ_ID:=Proj_08390_G
export MAF_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/test_data/maf
export FACETS_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/test_data/facets
export TARGETS_LIST:=/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist

# .maf input files JSON
muts.maf.txt:
	find $(MAF_DIR) -type f -name "*.muts.maf" | \
	xargs -I{} jq -n --arg path "{}" '{"class": "File", "path":$$path}' > muts.maf.txt
.PHONY: muts.maf.txt

# the copy_number_files input JSON
hisens.cncf.txt:
	find $(FACETS_DIR) -type f -name "*_hisens.cncf.txt" | \
	xargs -I{} jq -n --arg path "{}" '{"class": "File", "path":$$path}' > hisens.cncf.txt
.PHONY: hisens.cncf.txt

# the segmented copy number files
hisens.seg.txt:
	find $(FACETS_DIR) -type f -name "*_hisens.seg" | \
	xargs -I{} jq -n --arg path "{}" '{"class": "File", "path":$$path}' > hisens.seg.txt
.PHONY: hisens.seg.txt

# the input for the pipeline
export KNOWN_FUSIONS_FILE:=$(CURDIR)/ref/known_fusions_at_mskcc.txt
export ANALYST_FILE:=$(PROJ_ID).muts.maf
export ANALYST_GENE_CNA_FILE:=$(PROJ_ID).gene.cna.txt
export ARGOS_VERSION_STRING:=2.x
export IS_IMPACT:=True
export PORTAL_FILE:=data_mutations_extended.txt
export PORTAL_CNA_FILE:=data_CNA.txt
export SEGMENT_DATA_FILE:=$(PROJ_ID)_data_cna_hg19.seg
export CANCER_STUDY_IDENTIFIER:=$(PROJ_ID)
input.json: muts.maf.txt hisens.cncf.txt hisens.seg.txt
	if [ "$$(cat muts.maf.txt | wc -l)" -eq "0" ]; then echo ">>> ERROR: File muts.maf.txt is empty"; exit 1; fi
	if [ "$$(cat hisens.cncf.txt | wc -l)" -eq "0" ]; then echo ">>> ERROR: File muts.maf.txt is empty"; exit 1; fi
	if [ "$$(cat hisens.seg.txt | wc -l)" -eq "0" ]; then echo ">>> ERROR: File hisens.seg.txt is empty"; exit 1; fi
	jq -n \
	--slurpfile maf_files muts.maf.txt \
	--slurpfile hisens_cncfs hisens.cncf.txt \
	--slurpfile hisens_segs hisens.seg.txt \
	--arg cancer_study_identifier "$(CANCER_STUDY_IDENTIFIER)" \
	--arg segment_data_file "$(SEGMENT_DATA_FILE)" \
	--arg argos_version_string "$(ARGOS_VERSION_STRING)" \
	--arg is_impact "$(IS_IMPACT)" \
	--arg analyst_file "$(ANALYST_FILE)" \
	--arg analysis_gene_cna_file "$(ANALYST_GENE_CNA_FILE)" \
	--arg portal_file "$(PORTAL_FILE)" \
	--arg portal_CNA_file "$(PORTAL_CNA_FILE)" \
	--arg targets_list "$(TARGETS_LIST)" \
	'{"argos_version_string":$$argos_version_string,
	"segment_data_file":$$segment_data_file,
	"cancer_study_identifier":$$cancer_study_identifier,
	"is_impact":$$is_impact,
	"analyst_file":$$analyst_file,
	"portal_file":$$portal_file,
	"maf_files":$$maf_files,
	"portal_CNA_file": $$portal_CNA_file,
	"analysis_gene_cna_file": $$analysis_gene_cna_file,
	"hisens_cncfs":$$hisens_cncfs,
	"hisens_segs": $$hisens_segs,
	"targets_list":{"class": "File", "path": $$targets_list } }
	' > input.json
.PHONY: input.json

TMP_DIR:=$(CURDIR)/tmp/
OUTPUT_DIR:=$(CURDIR)/output/
CACHE_DIR:=$(CURDIR)/cache/

$(OUTPUT_DIR):
	mkdir -p "$(OUTPUT_DIR)"

# Run the CWL workflow
# example:
# make run PROJ_ID=10753_B MAF_DIR=/path/to/outputs/maf FACETS_DIR=/path/to/outputs/facets TARGETS_LIST=/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist OUTPUT_DIR=/path/to/helix_filters
INPUT_JSON:=input.json
DEBUG:=
run: $(INPUT_JSON) $(OUTPUT_DIR)
	module load singularity/3.3.0 && \
	cwl-runner $(DEBUG) \
	--parallel \
	--leave-tmpdir \
	--tmpdir-prefix $(TMP_DIR) \
	--outdir $(OUTPUT_DIR) \
	--cachedir $(CACHE_DIR) \
	--copy-outputs \
	--singularity \
	--preserve-environment PATH \
	--preserve-environment SINGULARITY_CACHEDIR \
	cwl/workflow.cwl $(INPUT_JSON)

# run the pure-Makefile version of the workflow
# export EXTRA_GROUPS:=
workflow:
	$(MAKE) -f workflow.makefile run

export FIXTURES_DIR:=/juno/work/ci/helix_filters_01/fixtures
test:
	export PATH=/opt/local/singularity/3.3.0/bin:$(PATH) && \
	python test.py

bash:
	module load singularity/3.3.0 && \
	bash

clean:
	rm -rf cache tmp
clean-all: clean
	rm -rf output portal analysis
