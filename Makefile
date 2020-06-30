export SHELL:=/bin/bash
.ONESHELL:
export SHELLOPTS:=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit
# export PATH:=$(CURDIR)/bin:$(PATH)
UNAME:=$(shell uname)

define help
This is the Makefile for helix filters

This repo contains scripts and workflows for usage with the Roslin pipeline in order to filter variant calling results

The subdir "roslin-post" is meant to include the main helix filter workflow + extra cBio Portal file generations (in development)

Example usage of this helix filter workflow:

make run PROJ_ID=My_Project MAF_DIR=/path/to/outputs/maf FACETS_DIR=/path/to/outputs/facets OUTPUT_DIR=/path/to/helix_filters TARGETS_LIST=/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist

check the file 'ref/roslin_resources.json' to find the correct target set for your assay type

Run the test suite:

make test

NOTE: requires the fixtures directory on juno

cBioPortal Validation
---------------------

- git clone the cBioPortal repo (git@github.com:cBioPortal/cbioportal.git)
- set up a virtual environment
$ python3 -m venv venv

- activate virtual environment
$ source venv/bin/activate

- install the libraries from requirements.txt with pip into the env (except the MySql ones)

- run a command like this against a demo workflow output directory;

cbioportal/core/src/main/scripts/importer$ ./validateData.py  --study_directory /juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/helix_filters_01/output/portal -n

endef
export help
help:
	@printf "$$help"
.PHONY : help

# ~~~~~ Install Dependencies ~~~~~ #
# NOTE: this is no longer used with `make run`, etc
# export PATH:=$(CURDIR)/conda/bin:$(CURDIR)/bin:$(PATH)
# unexport PYTHONPATH
# unexport PYTHONHOME

# ifeq ($(UNAME), Darwin)
# CONDASH:=Miniconda3-4.5.4-MacOSX-x86_64.sh
# endif
#
# ifeq ($(UNAME), Linux)
# CONDASH:=Miniconda3-4.5.4-Linux-x86_64.sh
# endif
#
# CONDAURL:=https://repo.anaconda.com/miniconda/$(CONDASH)
#
# conda:
# 	@set +e
# 	echo ">>> Setting up conda..."
# 	wget "$(CONDAURL)"
# 	bash "$(CONDASH)" -b -p conda
# 	rm -f "$(CONDASH)"
#
# install: conda
# 	conda install -y \
# 	conda-forge::jq=1.5
# 	pip install \
# 	cwltool==2.0.20200126090152 \
# 	cwlref-runner==1.0


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
TESTS_DATA_DIR:=/juno/work/ci/helix_filters_01/test_data/$(PROJ_ID)
DATA_DIR:=$(TESTS_DATA_DIR)
INPUTS_DIR:=$(DATA_DIR)/inputs
QC_DIR:=$(DATA_DIR)/qc
MAF_DIR:=$(DATA_DIR)/maf
BAM_DIR:=$(DATA_DIR)/bam
FACETS_DIR:=$(DATA_DIR)/facets
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
	--arg helix_filter_version "$(HELIX_FILTER_VERSION)" \
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
	"helix_filter_version": $$helix_filter_version,
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
export SINGULARITY_CACHEDIR:=/juno/work/ci/singularity_images
INPUT_JSON:=input.json
# pass debug flags here;
DEBUG:=
run: $(INPUT_JSON) $(OUTPUT_DIR)
	module load singularity/3.3.0 && \
	module load cwl/cwltool && \
	module load python/3.7.1 && \
	if [ ! -e "$(SINGULARITY_SIF)" ]; then $(MAKE) singularity-pull; fi && \
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


# ~~~~~ Run Facets CWL Workflow ~~~~~ #
FACETS_SNPS_VCF:=/juno/work/ci/resources/genomes/GRCh37/facets_snps/dbsnp_137.b37__RmDupsClean__plusPseudo50__DROP_SORT.vcf
PAIRING_FILE:=$(INPUTS_DIR)/$(PROJ_ID)_sample_pairing.txt
FACETS_OUTPUT_DIR:=$(OUTPUT_DIR)/facets-suite
$(FACETS_OUTPUT_DIR):
	mkdir -p "$(FACETS_OUTPUT_DIR)"
# file to hold facets pairing json data
# NOTE:only using first two pairs from file for debug here; full dataset takes 60min+ to run
facets-pairs.txt: $(PAIRING_FILE)
	module load jq
	cat $(PAIRING_FILE) | while IFS="$$(printf '\t')" read -r normal tumor; do
	pair_id="$${tumor}.$${normal}"
	tumor_bam="$(BAM_DIR)/$$tumor.rg.md.abra.printreads.bam"
	normal_bam="$(BAM_DIR)/$$normal.rg.md.abra.printreads.bam"
	pair_maf="$(MAF_DIR)/$${pair_id}.muts.maf"
	jq -n \
	--arg tumor_bam "$${tumor_bam}" \
	--arg normal_bam "$${normal_bam}" \
	--arg pair_id "$${pair_id}" \
	--arg pair_maf "$${pair_maf}" \
	'{
	"tumor_bam": { "class": "File", "path": $$tumor_bam },
	"normal_bam": { "class": "File", "path": $$normal_bam },
	"pair_maf": { "class": "File", "path": $$pair_maf },
	"pair_id": $$pair_id
	}
	'
	done > facets-pairs.txt
.PHONY: facets-pairs.txt

facets-input.json: facets-pairs.txt
	module load jq
	jq -n \
	--slurpfile pairs facets-pairs.txt \
	--arg snps_vcf "$(FACETS_SNPS_VCF)" \
	'{
	"pairs" :$$pairs,
	"snps_vcf": { "class": "File", "path": $$snps_vcf }
	}
	' > facets-input.json
.PHONY:facets-input.json

facets: facets-input.json $(FACETS_OUTPUT_DIR)
	module load singularity/3.3.0
	module load cwl/cwltool
	module load python/3.7.1
	cwl-runner \
	--parallel \
	--leave-tmpdir \
	--tmpdir-prefix $(TMP_DIR) \
	--outdir $(FACETS_OUTPUT_DIR) \
	--cachedir $(CACHE_DIR) \
	--copy-outputs \
	--singularity \
	--preserve-environment PATH \
	--preserve-environment SINGULARITY_CACHEDIR \
	cwl/facets-workflow.cwl facets-input.json








# ~~~~~ Container ~~~~~ #
# make the Docker container
GIT_NAME:=helix_filters_01
GIT_TAG:=$(shell git describe --tags --abbrev=0)
DOCKER_TAG:=mskcc/$(GIT_NAME):$(GIT_TAG)
docker-build:
	docker build -t "$(DOCKER_TAG)" .

# shell into the container to check that it looks right
docker-bash:
	docker run --rm -ti "$(DOCKER_TAG)" bash

# push the container to Dockerhub
# $ docker login --username=<username>
docker-push:
	docker push "$(DOCKER_TAG)"

# pull the Dockerhub container and convert to Singularity container
# NOTE: you cannot use a filename with a ':' as a Makefile target
SINGULARITY_SIF:=mskcc_$(GIT_NAME):$(GIT_TAG).sif
singularity-pull:
	unset SINGULARITY_CACHEDIR && \
	module load singularity/3.3.0 && \
	singularity pull --force --name "$(SINGULARITY_SIF)" docker://$(DOCKER_TAG)

# shell into the Singularity container to check that it looks right
singularity-shell:
	-module load singularity/3.3.0 && \
	singularity shell "$(SINGULARITY_SIF)"

OLD_TAG:=20.06.1
NEW_TAG:=20.06.2
update-container-tags:
	for i in $$(find cwl -type f -exec grep -l 'dockerPull: mskcc/helix_filters_01' {} \;); do \
	perl -i -pe 's/$(OLD_TAG)/$(NEW_TAG)/g' $$i ; \
	done

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
	if [ ! -e "$(SINGULARITY_SIF)" ]; then $(MAKE) singularity-pull; fi && \
	python3 test.py

# interactive session with environment populated
bash:
	module load singularity/3.3.0 && \
	module load python/3.7.1 && \
	module load cwl/cwltool && \
	module load jq && \
	bash

clean:
	rm -rf cache tmp
clean-all: clean
	rm -rf output portal analysis mutation_maf_files.txt facets_hisens_seg_files.txt facets_hisens_cncf_files.txt mutation_svs_txt_files.txt mutation_svs_maf_files.txt
