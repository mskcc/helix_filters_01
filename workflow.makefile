# Makefile to run the cBioPortal File Generation Workflow
# NOTE: designed to be invoked as sub-make from parent Makefile; this ensure the PATH and env are set correctly
export SHELL:=/bin/bash
.ONESHELL:
export SHELLOPTS:=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit

# check if the variable is already set e.g. from being invoked as sub-make
# TEST := $(if $(TEST),$(TEST),$(default value))

# output locations
OUTPUT_DIR:= $(if $(OUTPUT_DIR),$(OUTPUT_DIR),output)
ANALYSIS_DIR:= $(if $(ANALYSIS_DIR),$(ANALYSIS_DIR),$(OUTPUT_DIR)/analysis)
CBIO_PORTAL_DIR:= $(if $(CBIO_PORTAL_DIR),$(CBIO_PORTAL_DIR),$(OUTPUT_DIR)/portal)
CBIO_CASE_LIST_DIR:= $(if $(CBIO_CASE_LIST_DIR),$(CBIO_CASE_LIST_DIR),$(CBIO_PORTAL_DIR)/case_list)

# output parameters
PROJ_ID:= $(if $(PROJ_ID),$(PROJ_ID),project_id)
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

KNOWN_FUSIONS_FILE:= $(if $(KNOWN_FUSIONS_FILE),$(KNOWN_FUSIONS_FILE),$(CURDIR)/ref/known_fusions_at_mskcc.txt)

# reference files
ANALYST_FILE:= $(if $(ANALYST_FILE),$(ANALYST_FILE),$(PROJ_ID).muts.maf)
ANALYST_GENE_CNA_FILE:= $(if $(ANALYST_GENE_CNA_FILE),$(ANALYST_GENE_CNA_FILE),$(PROJ_ID).gene.cna.txt)

# files that will be output
CBIO_MUTATION_DATA_FILENAME:=data_mutations_extended.txt
CBIO_MUTATION_DATA_FILE:=$(CBIO_PORTAL_DIR)/$(CBIO_MUTATION_DATA_FILENAME)

CBIO_CNA_DATA_FILENAME:=data_CNA.txt
CBIO_CNA_DATA_FILE:=$(CBIO_PORTAL_DIR)/$(CBIO_CNA_DATA_FILENAME)

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

# input files
DEMO_DATA_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/test_data
DATA_CLINICAL_FILE:=$(DEMO_DATA_DIR)/inputs/Proj_08390_G_sample_data_clinical.txt
SAMPLE_SUMMARY_FILE:=$(DEMO_DATA_DIR)/qc/Proj_08390_G_SampleSummary.txt

# create output dirs
$(OUTPUT_DIR):
	mkdir -p "$(OUTPUT_DIR)"
$(ANALYSIS_DIR):
	mkdir -p "$(ANALYSIS_DIR)"
$(CBIO_PORTAL_DIR):
	mkdir -p "$(CBIO_PORTAL_DIR)"
$(CBIO_CASE_LIST_DIR):
	mkdir -p "$(CBIO_CASE_LIST_DIR)"

help:
	echo "help message goes here"

run: all

all: $(CBIO_CLINCIAL_PATIENT_DATA_FILE) $(CBIO_CLINICAL_SAMPLE_DATA_FILE) $(CBIO_META_STUDY_FILE) $(CBIO_CLINICAL_SAMPLE_META_FILE) $(CBIO_CLINCAL_PATIENT_META_FILE) $(CBIO_META_CNA_FILE) $(CBIO_META_FUSIONS_FILE) $(CBIO_META_MUTATIONS_FILE) $(CBIO_META_CNA_SEGMENTS_FILE) $(CBIO_CASES_ALL_FILE) $(CBIO_CASES_CNASEQ_FILE) $(CBIO_CASES_CNA_FILE) $(CBIO_CASES_SEQUENCED_FILE)

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
