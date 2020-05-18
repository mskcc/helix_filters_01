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

PROJ_ID:=Proj_08390_G
MAF_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/test_data/maf
FACETS_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/test_data/facets
TARGETS_LIST:=/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist
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

# the input for the pipeline
input.json: muts.maf.txt hisens.cncf.txt
	if [ "$$(cat muts.maf.txt | wc -l)" -eq "0" ]; then echo ">>> ERROR: File muts.maf.txt is empty"; exit 1; fi
	if [ "$$(cat hisens.cncf.txt | wc -l)" -eq "0" ]; then echo ">>> ERROR: File muts.maf.txt is empty"; exit 1; fi
	jq -n \
	--slurpfile maf_files muts.maf.txt \
	--slurpfile hisens_cncfs hisens.cncf.txt \
	--arg roslin_version_string "2.x" \
	--arg is_impact "True" \
	--arg analyst_file "$(PROJ_ID).muts.maf" \
	--arg analysis_gene_cna_file "$(PROJ_ID).gene.cna.txt" \
	--arg portal_file "data_mutations_extended.txt" \
	--arg portal_CNA_file "data_CNA.txt" \
	--arg targets_list "$(TARGETS_LIST)" \
	'{"roslin_version_string":$$roslin_version_string,
	"is_impact":$$is_impact,
	"analyst_file":$$analyst_file,
	"portal_file":$$portal_file,
	"maf_files":$$maf_files,
	"portal_CNA_file": $$portal_CNA_file,
	"analysis_gene_cna_file": $$analysis_gene_cna_file,
	"hisens_cncfs":$$hisens_cncfs,
	"targets_list":{"class": "File", "path": $$targets_list } }
	' > input.json
.PHONY: input.json

TMP_DIR:=$(CURDIR)/tmp/
OUTPUT_DIR:=$(CURDIR)/output/
CACHE_DIR:=$(CURDIR)/cache/

$(OUTPUT_DIR):
	mkdir -p "$(OUTPUT_DIR)"

# example:
# make run PROJ_ID=10753_B MAF_DIR=/path/to/outputs/maf FACETS_DIR=/path/to/outputs/facets TARGETS_LIST=/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist OUTPUT_DIR=/path/to/helix_filters
INPUT_JSON:=input.json
run: $(INPUT_JSON) $(OUTPUT_DIR)
	module load singularity/3.3.0 && \
	cwl-runner \
	--leave-tmpdir \
	--tmpdir-prefix $(TMP_DIR) \
	--outdir $(OUTPUT_DIR) \
	--cachedir $(CACHE_DIR) \
	--copy-outputs \
	--singularity \
	--preserve-environment PATH \
	--preserve-environment SINGULARITY_CACHEDIR \
	cwl/workflow.cwl $(INPUT_JSON)

test:
	module load singularity/3.3.0 && \
	python test.py

bash:
	bash

clean:
	rm -rf cache tmp
