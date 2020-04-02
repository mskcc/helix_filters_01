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
	nextflow run main.nf

clean:
	rm -f .nextflow.log*

clean-all: clean
	rm -rf work .nextflow
