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

run: install
	@source "$(ENV)"
	nextflow run main.nf \
	--targets IMPACT468_b37 \
	--maf_directory test_input_data/maf \
	--facets_directory test_input_data/facets \
	--containerDir /juno/work/ci/kellys5/projects/roslin-analysis-helper-dev/containers \
	-profile juno

clean:
	rm -f .nextflow.log*

clean-all: clean
	rm -rf work .nextflow
