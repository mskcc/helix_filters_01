SHELL:=/bin/bash
UNAME:=$(shell uname)
export SINGULARITY_CACHEDIR:=/juno/work/ci/singularity_images
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
FACETS_DIR:=../test_data/facets
TARGETS_LIST:=/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist
# .maf input files JSON
muts.maf.txt:
	ls -1 $(MAF_DIR)/*.muts.maf | \
	xargs -I{} jq -n --arg path "{}" '{"class": "File", "path":$$path}' > muts.maf.txt
.PHONY: muts.maf.txt

# the copy_number_files input JSON
hisens.cncf.txt:
	ls -1 $(FACETS_DIR)/*_hisens.cncf.txt | \
	xargs -I{} jq -n --arg path "{}" '{"class": "File", "path":$$path}' > hisens.cncf.txt
.PHONY: hisens.cncf.txt

# the input for the pipeline
input.json: muts.maf.txt hisens.cncf.txt
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
run: input.json
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
	cwl/workflow.cwl input.json

bash:
	bash
