SHELL:=/bin/bash
export NXF_ANSI_LOG:=false
export NXF_VER:=19.10.0
ENV=env.juno.sh
export PATH:=$(CURDIR):$(PATH)
.ONESHELL:

# ~~~~~ INSTALL & SETUP ~~~~~ #
# install Nextflow executable in current directory
./nextflow:
	@source "$(ENV)"
	curl -fsSL get.nextflow.io | bash

install: ./nextflow

INPUT_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/test_data
MAF_DIR:=$(INPUT_DIR)/maf
FACETS_DIR:=$(INPUT_DIR)/facets
INPUTS_YAML:=$(INPUT_DIR)/inputs/inputs.yaml

OUTPUT_DIR:=$(CURDIR)/output
PORTAL_DIR:=$(OUTPUT_DIR)/portal
ANALYSIS_DIR:=$(OUTPUT_DIR)/analysis

CONTAINER_DIR:=/juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/containers
run: install
	@source "$(ENV)"
	nextflow run main.nf \
	-resume \
	-profile juno \
	--targets IMPACT468_b37 \
	--inputDir $(INPUT_DIR) \
	--maf_directory $(MAF_DIR) \
	--facets_directory $(FACETS_DIR) \
	--containerDir $(CONTAINER_DIR) \
	--outputDir $(OUTPUT_DIR) \
	--outputPortalDir $(PORTAL_DIR) \
	--outputAnalysisDir $(ANALYSIS_DIR) \
	--inputs_yaml $(INPUTS_YAML)

clean:
	rm -f .nextflow.log*

clean-all: clean
	rm -rf work .nextflow

bash:
	@source "$(ENV)"
	bash

DOCKERTAG:=helix_filter
docker-build:
	cd containers/helix_filters_01 && \
	docker build -t "$(DOCKERTAG)" .
