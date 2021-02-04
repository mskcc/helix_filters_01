# Makefile to run the cBioPortal File Generation Workflow
# NOTE: designed to be invoked as sub-make from parent Makefile; this ensure the PATH and env are set correctly
export SHELL:=/bin/bash
.ONESHELL:
UNAME:=$(shell uname)
export SHELLOPTS:=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit
export SINGULARITY_CACHEDIR:=/juno/work/ci/singularity_images
export PATH:=$(CURDIR)/bin:$(PATH)

define help
This is the Makefile for running a prototype of the Roslin analysis post processing workflow for the creation of aggregate analysis files, and cBioPortal data and metadata files.

Usage
-----

This workflow can be called from the parent Makefile in this directory;

$ make workflow

Or it can be invoked directly (no extra args runs a test dataset);

$ make -f workflow.makefile run

Command line arguments should be provided to direct it to your Roslin pipeline outputs

$ make -f workflow.makefile run PIPELINE_RESULTS_DIR=/path/to/roslin/output TARGETS_LIST=/path/to/targets.ilist


Output
------

The output of this workflow looks like this:

output
├── analysis
│   ├── Proj_08390_G.gene.cna.txt
│   ├── Proj_08390_G.muts.maf
│   ├── Proj_08390_G.seg.cna.txt
│   └── Proj_08390_G.svs.maf
└── portal
    ├── case_list
    │   ├── cases_all.txt
    │   ├── cases_cnaseq.txt
    │   ├── cases_cna.txt
    │   └── cases_sequenced.txt
    ├── data_clinical_patient.txt
    ├── data_clinical_sample.txt
    ├── data_CNA.ascna.txt
    ├── data_CNA.scna.txt
    ├── data_CNA.txt
    ├── data_fusions.txt
    ├── data_mutations_extended.txt
    ├── meta_clinical_patient.txt
    ├── meta_clinical_sample.txt
    ├── meta_CNA.txt
    ├── meta_fusions.txt
    ├── meta_mutations_extended.txt
    ├── meta_study.txt
    ├── Proj_08390_G_data_cna_hg19.seg
    └── Proj_08390_G_meta_cna_hg19_seg.txt

3 directories, 23 files

Where 'Proj_08390_G' is your provided Project ID

endef

help:
	@printf "$$help"
.PHONY : help

# ~~~~~ debug ~~~~~ #
# interactive session for dev and debug
bash:
	module load singularity/3.3.0 && \
	bash

# checks if the variable is already set e.g. from being invoked as sub-make
# TEST := $(if $(TEST),$(TEST),$(default value))

# workflow parameters
PROJ_ID:= $(if $(PROJ_ID),$(PROJ_ID),Proj_08390_G)
PROJ_PI:=Dr. Jones
REQUEST_PI:=Dr. Franklin
PROJ_SHORT_NAME:=proj_id_short_name
PROJ_NAME:=project_name
PROJ_DESC:=Project description goes here
CANCER_TYPE:=MEL
CANCER_STUDY_IDENTIFIER:= $(if $(CANCER_STUDY_IDENTIFIER),$(CANCER_STUDY_IDENTIFIER),$(PROJ_ID))
ARGOS_VERSION_STRING:= $(if $(ARGOS_VERSION_STRING),$(ARGOS_VERSION_STRING),2.x)
IS_IMPACT:= $(if $(IS_IMPACT),$(IS_IMPACT),True)
EXTRA_PI_GROUPS:=
EXTRA_GROUPS_STR:=$(shell python -c 'print(" ".join([ "--extra-groups " + i for i in "$(EXTRA_PI_GROUPS)".split() ]))')

# input files and locations from the original Roslin / Argos pipeline run
# # a test data location on Juno; override this if you dont feel like setting all the other args directly
PIPELINE_RESULTS_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/test_data
INPUTS_DIR:=$(if $(INPUTS_DIR),$(INPUTS_DIR),$(PIPELINE_RESULTS_DIR)/inputs)
QC_DIR:=$(if $(QC_DIR),$(QC_DIR),$(PIPELINE_RESULTS_DIR)/qc)
MAF_DIR:= $(if $(MAF_DIR),$(MAF_DIR),$(PIPELINE_RESULTS_DIR)/maf)
FACETS_DIR:= $(if $(FACETS_DIR),$(FACETS_DIR),$(PIPELINE_RESULTS_DIR)/facets)
DATA_CLINICAL_FILE:=$(if $(DATA_CLINICAL_FILE),$(DATA_CLINICAL_FILE),$(INPUTS_DIR)/$(PROJ_ID)_sample_data_clinical.txt)
SAMPLE_SUMMARY_FILE:=$(if $(SAMPLE_SUMMARY_FILE),$(SAMPLE_SUMMARY_FILE),$(QC_DIR)/$(PROJ_ID)_SampleSummary.txt)

# output locations from this workflow
OUTPUT_DIR:= $(if $(OUTPUT_DIR),$(OUTPUT_DIR),output)
ANALYSIS_DIR:= $(if $(ANALYSIS_DIR),$(ANALYSIS_DIR),$(OUTPUT_DIR)/analysis)
CBIO_PORTAL_DIR:= $(if $(CBIO_PORTAL_DIR),$(CBIO_PORTAL_DIR),$(OUTPUT_DIR)/portal)
CBIO_CASE_LIST_DIR:= $(if $(CBIO_CASE_LIST_DIR),$(CBIO_CASE_LIST_DIR),$(CBIO_PORTAL_DIR)/case_list)

# reference files
KNOWN_FUSIONS_FILE:= $(if $(KNOWN_FUSIONS_FILE),$(KNOWN_FUSIONS_FILE),$(CURDIR)/ref/known_fusions_at_mskcc.txt)
# # You should ALWAYS override this:
TARGETS_LIST:=/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist
FACETS_CONTAINER:=$(CURDIR)/mskcc_roslin-variant-facets:1.6.3.sif

# files that will be output
CBIO_MUTATION_DATA_FILENAME:=data_mutations_extended.txt
CBIO_MUTATION_DATA_FILE:=$(CBIO_PORTAL_DIR)/$(CBIO_MUTATION_DATA_FILENAME)

CBIO_CNA_DATA_FILENAME:=data_CNA.txt
CBIO_CNA_DATA_FILE:=$(CBIO_PORTAL_DIR)/$(CBIO_CNA_DATA_FILENAME)
CBIO_CNA_ASCNA_DATA_FILE:=$(CBIO_PORTAL_DIR)/data_CNA.ascna.txt
CBIO_CNA_SCNA_DATA_FILE:=$(CBIO_PORTAL_DIR)/data_CNA.scna.txt


CBIO_SEGMENT_DATA_FILENAME:=$(PROJ_ID)_data_cna_hg19.seg
CBIO_SEGMENT_DATA_FILE:=$(CBIO_PORTAL_DIR)/$(CBIO_SEGMENT_DATA_FILENAME)

CBIO_FUSION_DATA_FILENAME:=data_fusions.txt
CBIO_FUSION_DATA_FILE:=$(CBIO_PORTAL_DIR)/$(CBIO_FUSION_DATA_FILENAME)

CBIO_CLINCIAL_PATIENT_DATA_FILENAME:=data_clinical_patient.txt
CBIO_CLINCIAL_PATIENT_DATA_FILE:=$(CBIO_PORTAL_DIR)/$(CBIO_CLINCIAL_PATIENT_DATA_FILENAME)

CBIO_CLINICAL_SAMPLE_DATA_FILENAME:=data_clinical_sample.txt
CBIO_CLINICAL_SAMPLE_DATA_FILE:=$(CBIO_PORTAL_DIR)/$(CBIO_CLINICAL_SAMPLE_DATA_FILENAME)

CBIO_CLINICAL_SAMPLE_META_FILE:=$(CBIO_PORTAL_DIR)/meta_clinical_sample.txt
CBIO_CLINCAL_PATIENT_META_FILE:=$(CBIO_PORTAL_DIR)/meta_clinical_patient.txt
CBIO_META_STUDY_FILE:=$(CBIO_PORTAL_DIR)/meta_study.txt
CBIO_META_CNA_FILE:=$(CBIO_PORTAL_DIR)/meta_CNA.txt
CBIO_META_FUSIONS_FILE:=$(CBIO_PORTAL_DIR)/meta_fusions.txt
CBIO_META_MUTATIONS_FILE:=$(CBIO_PORTAL_DIR)/meta_mutations_extended.txt
CBIO_META_CNA_SEGMENTS_FILE:=$(CBIO_PORTAL_DIR)/$(PROJ_ID)_meta_cna_hg19_seg.txt
CBIO_CASES_ALL_FILE:=$(CBIO_CASE_LIST_DIR)/cases_all.txt
CBIO_CASES_CNASEQ_FILE:=$(CBIO_CASE_LIST_DIR)/cases_cnaseq.txt
CBIO_CASES_CNA_FILE:=$(CBIO_CASE_LIST_DIR)/cases_cna.txt
CBIO_CASES_SEQUENCED_FILE:=$(CBIO_CASE_LIST_DIR)/cases_sequenced.txt


# files for analysis output
# ANALYST_FILE:= $(if $(ANALYST_FILE),$(ANALYST_FILE),$(ANALYSIS_DIR)/$(PROJ_ID).muts.maf)
# ANALYST_GENE_CNA_FILE:= $(if $(ANALYST_GENE_CNA_FILE),$(ANALYST_GENE_CNA_FILE),$(ANALYSIS_DIR)/$(PROJ_ID).gene.cna.txt)
ANALYSIS_SV_FILE:=$(ANALYSIS_DIR)/$(PROJ_ID).svs.maf
ANALYSIS_MUTATIONS_FILE:=$(ANALYSIS_DIR)/$(PROJ_ID).muts.maf
ANALYSIS_GENE_CNA_FILE:=$(ANALYSIS_DIR)/$(PROJ_ID).gene.cna.txt
ANALYSIS_SEGMENT_CNA_FILE:=$(ANALYSIS_DIR)/$(PROJ_ID).seg.cna.txt
# _data_cna_hg19.seg CBIO_SEGMENT_DATA_FILE



# create output dirs
$(OUTPUT_DIR):
	mkdir -p "$(OUTPUT_DIR)"
$(ANALYSIS_DIR):
	mkdir -p "$(ANALYSIS_DIR)"
$(CBIO_PORTAL_DIR):
	mkdir -p "$(CBIO_PORTAL_DIR)"
$(CBIO_CASE_LIST_DIR):
	mkdir -p "$(CBIO_CASE_LIST_DIR)"


run: validate-inputs all

validate-inputs: $(MAF_DIR) $(FACETS_DIR) $(DATA_CLINICAL_FILE) $(SAMPLE_SUMMARY_FILE)

all: $(CBIO_CLINCIAL_PATIENT_DATA_FILE) $(CBIO_CLINICAL_SAMPLE_DATA_FILE) $(CBIO_META_STUDY_FILE) $(CBIO_CLINICAL_SAMPLE_META_FILE) $(CBIO_CLINCAL_PATIENT_META_FILE) $(CBIO_META_CNA_FILE) $(CBIO_META_FUSIONS_FILE) $(CBIO_META_MUTATIONS_FILE) $(CBIO_META_CNA_SEGMENTS_FILE) $(CBIO_CASES_ALL_FILE) $(CBIO_CASES_CNASEQ_FILE) $(CBIO_CASES_CNA_FILE) $(CBIO_CASES_SEQUENCED_FILE) $(CBIO_FUSION_DATA_FILE) $(ANALYSIS_SV_FILE) $(CBIO_SEGMENT_DATA_FILE) $(ANALYSIS_MUTATIONS_FILE) $(CBIO_MUTATION_DATA_FILE) $(CBIO_CNA_DATA_FILE) $(ANALYSIS_GENE_CNA_FILE) $(CBIO_CNA_ASCNA_DATA_FILE) $(CBIO_CNA_SCNA_DATA_FILE) $(ANALYSIS_SEGMENT_CNA_FILE)

# data_clinical_patient.txt
$(CBIO_CLINCIAL_PATIENT_DATA_FILE): $(CBIO_PORTAL_DIR) $(DATA_CLINICAL_FILE)
	generate_cbioPortal_files.py \
	patient \
	--data-clinical-file "$(DATA_CLINICAL_FILE)" \
	--output "$(CBIO_CLINCIAL_PATIENT_DATA_FILE)"

# data_clinical_sample.txt
$(CBIO_CLINICAL_SAMPLE_DATA_FILE): $(CBIO_PORTAL_DIR) $(SAMPLE_SUMMARY_FILE) $(DATA_CLINICAL_FILE)
	generate_cbioPortal_files.py \
	sample \
	--data-clinical-file "$(DATA_CLINICAL_FILE)" \
	--sample-summary-file "$(SAMPLE_SUMMARY_FILE)" \
	--project-pi "$(PROJ_PI)" \
	--request-pi "$(REQUEST_PI)" \
	--output "$(CBIO_CLINICAL_SAMPLE_DATA_FILE)"

# data_CNA.txt, data_CNA.ascna.txt, data_CNA.scna.txt ; PORTAL_CNA_FILE ; ANALYSIS_GENE_CNA_FILE
# from facets workflow ; copy_number.cwl
$(CBIO_CNA_DATA_FILE) $(ANALYSIS_GENE_CNA_FILE) $(CBIO_CNA_ASCNA_DATA_FILE) $(CBIO_CNA_SCNA_DATA_FILE): $(CBIO_PORTAL_DIR) $(ANALYSIS_DIR)
	module load singularity/3.3.0
	files=( $(FACETS_DIR)/*_hisens.cncf.txt )
	singularity exec \
	-B /juno/work \
	-B "$(CURDIR)" \
	-B "$(FACETS_DIR)" \
	-B "$(CBIO_PORTAL_DIR)" \
	"$(FACETS_CONTAINER)" \
	/bin/bash -c "
	python /usr/bin/facets-suite/facets geneLevel --cnaMatrix -o $(CBIO_CNA_DATA_FILE) --targetFile $(TARGETS_LIST) -f $${files[*]}
	"
	cp "$(CBIO_CNA_DATA_FILE)" "$(ANALYSIS_GENE_CNA_FILE)"

# data_mutations_extended.txt ; PORTAL_FILE ; $(PROJ_ID).muts.maf
# from maf_filter.cwl maf_filter.py; TODO: split this into a separate script because the script outputs two files currently
# need to strip comments, concat tables, then pass to filter script
$(ANALYSIS_MUTATIONS_FILE) $(CBIO_MUTATION_DATA_FILE): $(CBIO_PORTAL_DIR) $(ANALYSIS_DIR)
	files=( $(MAF_DIR)/*.muts.maf )
	set +o pipefail
	grep -v '#' $${files[0]} | head -1 > tmp1.txt
	for i in $${files[@]}; do
	grep -v '#' $$i | tail -n +2 >> tmp1.txt
	done
	maf_filter.py \
	tmp1.txt \
	2.x \
	True \
	"$(ANALYSIS_MUTATIONS_FILE)" \
	"$(CBIO_MUTATION_DATA_FILE)"
	rm -f tmp1.txt

# $(PROJ_ID)_data_cna_hg19.seg, $(PROJ_ID).seg.cna.txt # from reduce_sig_figs.cwl + concat.cwl
$(CBIO_SEGMENT_DATA_FILE) $(ANALYSIS_SEGMENT_CNA_FILE): $(CBIO_PORTAL_DIR) $(ANALYSIS_DIR)
	files=( $(FACETS_DIR)/*_hisens.seg )
	head -1 $${files[0]} > tmp2.txt
	for i in $${files[@]}; do
	tail -n +2 $$i >> tmp2.txt
	done
	reduce_sig_figs_seg.mean.py tmp2.txt > "$(CBIO_SEGMENT_DATA_FILE)"
	cp "$(CBIO_SEGMENT_DATA_FILE)" "$(ANALYSIS_SEGMENT_CNA_FILE)"
	rm -f tmp2.txt

# meta_study.txt
$(CBIO_META_STUDY_FILE): $(CBIO_PORTAL_DIR)
	generate_cbioPortal_files.py \
	study \
	--cancer-study-id "$(PROJ_ID)" \
	--name "$(PROJ_NAME)" \
	--short-name "$(PROJ_SHORT_NAME)" \
	--type-of-cancer "$(CANCER_TYPE)" \
	--description "$(PROJ_DESC)" \
	--output "$(CBIO_META_STUDY_FILE)" \
	$(EXTRA_GROUPS_STR)

# meta_clinical_sample.txt
$(CBIO_CLINICAL_SAMPLE_META_FILE): $(CBIO_PORTAL_DIR)
	generate_cbioPortal_files.py \
	meta_sample \
	--cancer-study-id "$(PROJ_ID)" \
	--sample-data-filename $(CBIO_CLINICAL_SAMPLE_DATA_FILENAME) \
	--output "$(CBIO_CLINICAL_SAMPLE_META_FILE)"

# meta_clinical_patient.txt
$(CBIO_CLINCAL_PATIENT_META_FILE): $(CBIO_PORTAL_DIR)
	generate_cbioPortal_files.py \
	meta_patient \
	--cancer-study-id "$(PROJ_ID)" \
	--patient-data-filename "$(CBIO_CLINCIAL_PATIENT_DATA_FILENAME)" \
	--output "$(CBIO_CLINCAL_PATIENT_META_FILE)"

# meta_CNA.txt
$(CBIO_META_CNA_FILE): $(CBIO_PORTAL_DIR)
	generate_cbioPortal_files.py \
	meta_cna \
	--cancer-study-id "$(PROJ_ID)" \
	--cna-data-filename "$(CBIO_CNA_DATA_FILENAME)" \
	--output "$(CBIO_META_CNA_FILE)"

# meta_fusions.txt
$(CBIO_META_FUSIONS_FILE): $(CBIO_PORTAL_DIR)
	generate_cbioPortal_files.py \
	meta_fusion \
	--cancer-study-id "$(PROJ_ID)" \
	--fusion-data-filename "$(CBIO_FUSION_DATA_FILENAME)" \
	--output "$(CBIO_META_FUSIONS_FILE)"

# meta_mutations_extended.txt
$(CBIO_META_MUTATIONS_FILE): $(CBIO_PORTAL_DIR)
	generate_cbioPortal_files.py \
	meta_mutations \
	--cancer-study-id "$(PROJ_ID)" \
	--mutations-data-filename "$(CBIO_MUTATION_DATA_FILENAME)" \
	--output "$(CBIO_META_MUTATIONS_FILE)"

# <project_id>_meta_cna_hg19_seg.txt
$(CBIO_META_CNA_SEGMENTS_FILE): $(CBIO_PORTAL_DIR)
	generate_cbioPortal_files.py \
	meta_segments \
	--cancer-study-id "$(PROJ_ID)" \
	--output "$(CBIO_META_CNA_SEGMENTS_FILE)" \
	--segmented-data-file "$(CBIO_SEGMENT_DATA_FILENAME)"

# cases_all.txt
$(CBIO_CASES_ALL_FILE): $(CBIO_CASE_LIST_DIR) $(DATA_CLINICAL_FILE)
	generate_cbioPortal_files.py \
	cases_all  \
	--cancer-study-id "$(PROJ_ID)" \
	--data-clinical-file "$(DATA_CLINICAL_FILE)" \
	--output "$(CBIO_CASES_ALL_FILE)"

# cases_cnaseq.txt
$(CBIO_CASES_CNASEQ_FILE): $(CBIO_CASE_LIST_DIR) $(DATA_CLINICAL_FILE)
	generate_cbioPortal_files.py \
	cases_cnaseq \
	--cancer-study-id "$(PROJ_ID)" \
	--data-clinical-file "$(DATA_CLINICAL_FILE)" \
	--output "$(CBIO_CASES_CNASEQ_FILE)"

# cases_cna.txt
$(CBIO_CASES_CNA_FILE): $(CBIO_CASE_LIST_DIR) $(DATA_CLINICAL_FILE)
	generate_cbioPortal_files.py \
	cases_cna \
	--cancer-study-id "$(PROJ_ID)" \
	--data-clinical-file "$(DATA_CLINICAL_FILE)" \
	--output "$(CBIO_CASES_CNA_FILE)"

# cases_sequenced.txt
$(CBIO_CASES_SEQUENCED_FILE): $(CBIO_CASE_LIST_DIR) $(DATA_CLINICAL_FILE)
	generate_cbioPortal_files.py \
	cases_sequenced \
	--cancer-study-id "$(PROJ_ID)" \
	--data-clinical-file "$(DATA_CLINICAL_FILE)" \
	--output "$(CBIO_CASES_SEQUENCED_FILE)"

# data_fusions.txt
# NOTE: using a bash array here for convenience, watch out for old old versions of bash
$(CBIO_FUSION_DATA_FILE): $(MAF_DIR)
	files=( $(MAF_DIR)/*.svs.pass.vep.portal.txt )
	head -1 $${files[0]} > tmp3.txt
	for i in $${files[@]}; do
	tail -n +2 $$i >> tmp3.txt
	done
	fusion_filter.py tmp3.txt "$(CBIO_FUSION_DATA_FILE)" "$(KNOWN_FUSIONS_FILE)"
	rm -f tmp3.txt

# $(PROJ_ID).svs.maf
$(ANALYSIS_SV_FILE): $(ANALYSIS_DIR)
	files=( $(MAF_DIR)/*.svs.pass.vep.maf )
	echo '# Version: $(ARGOS_VERSION_STRING)' > "$(ANALYSIS_SV_FILE)"
	grep -v '#' $${files[0]} | head -1 > $(ANALYSIS_SV_FILE)
	for i in $${files[@]}; do
	grep -v '#' $$i | tail -n +2 >> "$(ANALYSIS_SV_FILE)"
	done

test: $(CBIO_CNA_DATA_FILE) $(ANALYSIS_GENE_CNA_FILE)
