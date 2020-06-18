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

# ~~~~~ Install Dependencies ~~~~~ #
UNAME:=$(shell uname)
export SINGULARITY_CACHEDIR:=/juno/work/ci/singularity_images
# export PATH:=$(CURDIR)/conda/bin:$(CURDIR)/bin:$(PATH)
export PATH:=$(CURDIR)/bin:$(PATH)
# unexport PYTHONPATH
# unexport PYTHONHOME

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


# ~~~~~ Setup Up and Run the CWL Workflow ~~~~~ #

# example values

# project_id
PROJ_ID:=Proj_08390_G
# project_pi
PROJ_PI:=Dr. Jones
# request_pi
REQUEST_PI:=Dr. Franklin
# project_short_name
PROJ_SHORT_NAME:=$(PROJ_ID)
# project_name
PROJ_NAME:=$(PROJ_ID)
# project_description
PROJ_DESC:=Project description
# cancer_type
CANCER_TYPE:=MEL
# cancer_study_identifier
CANCER_STUDY_IDENTIFIER:=$(PROJ_ID)
# argos_version_string
ARGOS_VERSION_STRING:=2.x
# is_impact
IS_IMPACT:=True
# extra_pi_groups
# EXTRA_PI_GROUPS:=
# analysis_segment_cna_filename
ANALYSIS_SEGMENT_CNA_FILE:=$(PROJ_ID).seg.cna.txt
# analysis_sv_filename
ANALYSIS_SV_FILE:=$(PROJ_ID).svs.maf
# analysis_gene_cna_filename
ANALYSIS_GENE_CNA_FILENAME:=$(PROJ_ID).gene.cna.txt
# analysis_mutations_filename
ANALYSIS_MUTATIONS_FILENAME:=$(PROJ_ID).muts.maf
# cbio_segment_data_filename
CBIO_SEGMENT_DATA_FILENAME:=$(PROJ_ID)_data_cna_hg19.seg
# cbio_meta_cna_segments_filename
CBIO_META_CNA_SEGMENTS_FILENAME:=$(PROJ_ID)_meta_cna_hg19_seg.txt


# reference files
# known_fusions_file
KNOWN_FUSIONS_FILE:=$(CURDIR)/ref/known_fusions_at_mskcc.txt
# targets_list
TARGETS_LIST:=/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist
# helix_filter_version
HELIX_FILTER_VERSION:=$(shell git describe --all --long | sed -e 's|.*/\(.*\)|\1|g')
# argos_version_string
ARGOS_VERSION_STRING:=2.x

# demo locations for use for development; set these from the command line for real-world usage (not used for CWL input)
INPUTS_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/test_data/inputs
QC_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/test_data/qc
MAF_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/test_data/maf
FACETS_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/test_data/facets
DATA_CLINICAL_FILE:=$(INPUTS_DIR)/$(PROJ_ID)_sample_data_clinical.txt
SAMPLE_SUMMARY_FILE:=$(QC_DIR)/$(PROJ_ID)_SampleSummary.txt
# Need to create some psuedo-JSON files for use in creating the input.json

# .maf input files JSON muts.maf.txt
mutation_maf_files.txt:
	module load jq/1.6 && \
	find $(MAF_DIR) -type f -name "*.muts.maf" | \
	xargs -I{} jq -n --arg path "{}" '{"class": "File", "path":$$path}' > mutation_maf_files.txt
.PHONY: mutation_maf_files.txt

# the segmented copy number files hisens.seg.txt
facets_hisens_seg_files.txt:
	module load jq/1.6 && \
	find $(FACETS_DIR) -type f -name "*_hisens.seg" | \
	xargs -I{} jq -n --arg path "{}" '{"class": "File", "path":$$path}' > facets_hisens_seg_files.txt
.PHONY: facets_hisens_seg_files.txt

# the copy_number_files input JSON hisens.cncf.txt
facets_hisens_cncf_files.txt:
	module load jq/1.6 && \
	find $(FACETS_DIR) -type f -name "*_hisens.cncf.txt" | \
	xargs -I{} jq -n --arg path "{}" '{"class": "File", "path":$$path}' > facets_hisens_cncf_files.txt
.PHONY: facets_hisens_cncf_files.txt

mutation_svs_txt_files.txt:
	module load jq/1.6 && \
	find $(MAF_DIR) -type f -name "*.svs.pass.vep.portal.txt" | \
	xargs -I{} jq -n --arg path "{}" '{"class": "File", "path":$$path}' > mutation_svs_txt_files.txt
.PHONY: mutation_svs_txt_files.txt

mutation_svs_maf_files.txt:
	module load jq/1.6 && \
	find $(MAF_DIR) -type f -name "*.svs.pass.vep.maf" | \
	xargs -I{} jq -n --arg path "{}" '{"class": "File", "path":$$path}' > mutation_svs_maf_files.txt
.PHONY: mutation_svs_maf_files.txt


# input file for the CWL workflow; omits some workflow.cwl input fields that have static default values
input.json: mutation_maf_files.txt facets_hisens_seg_files.txt facets_hisens_cncf_files.txt mutation_svs_txt_files.txt mutation_svs_maf_files.txt
	if [ "$$(cat mutation_maf_files.txt | wc -l)" -eq "0" ]; then echo ">>> ERROR: File mutation_maf_files.txt is empty"; exit 1; fi
	if [ "$$(cat facets_hisens_seg_files.txt | wc -l)" -eq "0" ]; then echo ">>> ERROR: File facets_hisens_seg_files.txt is empty"; exit 1; fi
	if [ "$$(cat facets_hisens_cncf_files.txt | wc -l)" -eq "0" ]; then echo ">>> ERROR: File facets_hisens_cncf_files.txt is empty"; exit 1; fi
	if [ "$$(cat mutation_svs_txt_files.txt | wc -l)" -eq "0" ]; then echo ">>> ERROR: File mutation_svs_txt_files.txt is empty"; exit 1; fi
	if [ "$$(cat mutation_svs_maf_files.txt | wc -l)" -eq "0" ]; then echo ">>> ERROR: File mutation_svs_maf_files.txt is empty"; exit 1; fi
	module load jq/1.6 && \
	jq -n \
	--slurpfile mutation_maf_files mutation_maf_files.txt \
	--slurpfile facets_hisens_seg_files facets_hisens_seg_files.txt \
	--slurpfile facets_hisens_cncf_files facets_hisens_cncf_files.txt \
	--slurpfile mutation_svs_txt_files mutation_svs_txt_files.txt \
	--slurpfile mutation_svs_maf_files mutation_svs_maf_files.txt \
	--arg project_id "$(PROJ_ID)" \
	--arg project_pi "$(PROJ_PI)" \
	--arg request_pi "$(REQUEST_PI)" \
	--arg project_short_name "$(PROJ_SHORT_NAME)" \
	--arg project_name "$(PROJ_NAME)" \
	--arg project_description "$(PROJ_DESC)" \
	--arg cancer_type "$(CANCER_TYPE)" \
	--arg cancer_study_identifier "$(CANCER_STUDY_IDENTIFIER)" \
	--arg argos_version_string "$(ARGOS_VERSION_STRING)" \
	--arg is_impact "$(IS_IMPACT)" \
	--arg analysis_segment_cna_filename "$(ANALYSIS_SEGMENT_CNA_FILE)" \
	--arg analysis_sv_filename "$(ANALYSIS_SV_FILE)" \
	--arg analysis_gene_cna_filename "$(ANALYSIS_GENE_CNA_FILENAME)" \
	--arg analysis_mutations_filename "$(ANALYSIS_MUTATIONS_FILENAME)" \
	--arg cbio_segment_data_filename "$(CBIO_SEGMENT_DATA_FILENAME)" \
	--arg cbio_meta_cna_segments_filename "$(CBIO_META_CNA_SEGMENTS_FILENAME)" \
	--arg targets_list "$(TARGETS_LIST)" \
	--arg known_fusions_file "$(KNOWN_FUSIONS_FILE)" \
	--arg data_clinical_file "$(DATA_CLINICAL_FILE)" \
	--arg sample_summary_file "$(SAMPLE_SUMMARY_FILE)" \
	'{
	"mutation_maf_files": $$mutation_maf_files,
	"facets_hisens_seg_files": $$facets_hisens_seg_files,
	"facets_hisens_cncf_files": $$facets_hisens_cncf_files,
	"mutation_svs_txt_files": $$mutation_svs_txt_files,
	"mutation_svs_maf_files": $$mutation_svs_maf_files,
	"project_id": $$project_id,
	"project_pi": $$project_pi,
	"request_pi": $$request_pi,
	"project_short_name": $$project_short_name,
	"project_name": $$project_name,
	"project_description": $$project_description,
	"cancer_type": $$cancer_type,
	"cancer_study_identifier": $$cancer_study_identifier,
	"argos_version_string": $$argos_version_string,
	"is_impact": $$is_impact,
	"analysis_segment_cna_filename": $$analysis_segment_cna_filename,
	"analysis_sv_filename": $$analysis_sv_filename,
	"analysis_gene_cna_filename": $$analysis_gene_cna_filename,
	"analysis_mutations_filename": $$analysis_mutations_filename,
	"cbio_segment_data_filename": $$cbio_segment_data_filename,
	"cbio_meta_cna_segments_filename": $$cbio_meta_cna_segments_filename,
	"targets_list": {"class": "File", "path": $$targets_list},
	"known_fusions_file": {"class": "File", "path": $$known_fusions_file},
	"data_clinical_file": {"class": "File", "path": $$data_clinical_file},
	"sample_summary_file": {"class": "File", "path": $$sample_summary_file}
	}
	' > input.json
.PHONY: input.json

# locations for running the CWL workflow
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
	module load cwl/cwltool && \
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


# ~~~~~ Container ~~~~~ #
# make the Docker container
GIT_NAME:=helix_filters_01
GIT_TAG:=$(shell git describe --tags --abbrev=0)
DOCKER_TAG:=mskcc/$(GIT_NAME):$(GIT_TAG)
docker-build:
	docker build -t "$(DOCKER_TAG)" .
docker-bash:
	docker run --rm -ti "$(DOCKER_TAG)" bash

# $ docker login --username=<username>
docker-push:
	docker push "$(DOCKER_TAG)"
# ~~~~~ Debug & Development ~~~~~ #

# run the pure-Makefile prototype reference version of the workflow
workflow:
	$(MAKE) -f workflow.makefile run

workflow-test:
	$(MAKE) -f workflow.makefile test

# Run the test suite
export FIXTURES_DIR:=/juno/work/ci/helix_filters_01/fixtures
test:
	export PATH=/opt/local/singularity/3.3.0/bin:$(PATH) && \
	module load python/3.7.1 && \
	module load cwl/cwltool && \
	python3 test.py

# interactive session with environment populated
bash:
	module load singularity/3.3.0 && \
	bash

clean:
	rm -rf cache tmp
clean-all: clean
	rm -rf output portal analysis mutation_maf_files.txt facets_hisens_seg_files.txt facets_hisens_cncf_files.txt mutation_svs_txt_files.txt mutation_svs_maf_files.txt
