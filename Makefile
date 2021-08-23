export SHELL:=/bin/bash
.ONESHELL:
# export SHELLOPTS:=$(if $(SHELLOPTS),$(SHELLOPTS):)pipefail:errexit
# export PATH:=$(CURDIR)/bin:$(PATH)
UNAME:=$(shell uname)

define help
This repository contains scripts for usage with [`pluto-cwl`](https://github.com/mskcc/pluto-cwl) for running post-pipeline data formatting and lightweight analysis.

Run the test suite:

```
make test
```

NOTE: requires the fixtures directory on juno

Run an individual test script:

```
# initialize the environment
make bash

# run the test script you want to dev on
python3 tests/test_calc-tmb.py
```

cBioPortal Validation
---------------------

Files generated from here can be validated in cBioPortal with this method:

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
export PATH:=$(CURDIR)/conda/bin:$(CURDIR)/bin:$(PATH)
unexport PYTHONPATH
unexport PYTHONHOME

ifeq ($(UNAME), Darwin)
CONDASH:=Miniconda3-4.5.4-MacOSX-x86_64.sh
endif

ifeq ($(UNAME), Linux)
CONDASH:=Miniconda3-4.5.4-Linux-x86_64.sh
endif

CONDAURL:=https://repo.anaconda.com/miniconda/$(CONDASH)

conda:
	@set +e
	echo ">>> Setting up conda..."
	wget "$(CONDAURL)"
	bash "$(CONDASH)" -b -p conda
	rm -f "$(CONDASH)"

install: conda
	conda install -y \
	anaconda::numpy=1.19.1 \
	anaconda::pandas=1.1.3
	git submodule update --init --recursive



# ~~~~~ Container ~~~~~ #
# make the Docker container
GIT_NAME:=helix_filters_01
# this should default to 'latest'
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

FACETS_DOCKERTAG:=stevekm/facets-suite:dev
FACETS_SIF:=stevekm_facets-suite:dev.sif
singularity-pull-facets:
	unset SINGULARITY_CACHEDIR && \
	module load singularity/3.3.0 && \
	singularity pull --force --name "$(FACETS_SIF)" docker://$(FACETS_DOCKERTAG)

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
# Run the test suite
export FIXTURES_DIR:=/juno/work/ci/helix_filters_01/fixtures
# run tests in parallel;
# $ make test -j 4
TESTS:=$(shell ls tests/test_*.py)
$(TESTS):
	module load singularity/3.3.0 && module load python/3.7.1 && module load cwl/cwltool && echo $@; python3 $@
.PHONY: $(TESTS)
test: $(TESTS)

# for some reason the test recipe is not running all tests....
test2:
	module load singularity/3.3.0 && \
	module load python/3.7.1 && \
	module load cwl/cwltool && \
	if [ ! -e "$(SINGULARITY_SIF)" ]; then $(MAKE) singularity-pull; fi && \
	for i in tests/test_*.py; do echo $$i; $$i; done

# TODO: figure out why this is missing some tests
test-old:
	export PATH=/opt/local/singularity/3.3.0/bin:$(PATH) && \
	module load python/3.7.1 && \
	module load cwl/cwltool && \
	if [ ! -e "$(SINGULARITY_SIF)" ]; then $(MAKE) singularity-pull; fi && \
	python3 test.py

# # run the pure-Makefile prototype reference version of the workflow
# workflow:
# 	$(MAKE) -f workflow.makefile run
#
# workflow-test:
# 	$(MAKE) -f workflow.makefile test

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
