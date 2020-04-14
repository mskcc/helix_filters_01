SHELL:=/bin/bash
UNAME:=$(shell uname)
export PATH:=$(CURDIR)/conda/bin:$(CURDIR)/bin:$(PATH)
unexport PYTHONPATH
unexport PYTHONHOME
.ONESHELL:

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

PROJ_ID:=Project_1
MAF_DIR:=../test_data/maf
run:
	set -x
	ls -1 $(MAF_DIR)/*.muts.maf | \
	xargs -I{} jq -n --arg path "{}" '{"class": "File", "path":$$path}' | \
	jq -s '.'  > files.json && \
	jq -n \
	--slurpfile files files.json \
	--arg roslin_version_string "2.x" \
	--arg is_impact "True" \
	--arg analyst_file "$(PROJ_ID).muts.maf" \
	--arg portal_file "data_mutations_extended.txt" \
	'{"roslin_version_string":$$roslin_version_string,
	"is_impact":$$is_impact,
	"analyst_file":$$analyst_file,
	"portal_file":$$portal_file,
	"maf_files":$$files}
	' \
	> input.json
# cwl-runner cwl/maf_filter.cwl input.json

# --arg maf_file "$(maf_file)" \
# "maf_file": {"class": "File", "path":$$maf_file} }

bash:
	bash
