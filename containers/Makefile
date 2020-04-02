SHELL:=/bin/bash
define help
This is the Makefile for building containers

To build a Singularity container on your local computer (e.g. macOS) you first need to use Docker to build a container with Singularity installed. This will be used to build Singularity containers. A recipe for a Docker container with Singularity is included, build it with:

make singularity-docker-container-build

This is required for building Singularity containers.

To build a Singularity container from a recipe subdir in this directory, use a command like

make singularity-build-docker VAR=<dirname>

Example:

make singularity-build-docker VAR=facets-1.6.3

NOTE: do not include trailing slash on the dirname
endef
export help
help:
	@printf "$$help"
.PHONY : help

# this should be the name of a subdir in this dir
export VAR:=
export DOCKERTAG:=$(VAR)
docker-build:
	cd "$(VAR)" && docker build -t "$(DOCKERTAG)" .


# build the Docker container with Singularity in it
export SINGULARITY_DOCKERTAG:=singularity-3.3.0
singularity-docker-container-build:
	cd Singularity-3.3.0 && \
	docker build -t "$(SINGULARITY_DOCKERTAG)" .

# for debug; enter the docker container
singularity-docker-container-run:
	docker run --rm -ti -v "$(CURDIR):/image" "$(SINGULARITY_DOCKERTAG)" bash

# build the singularity container
# on HPC: module load singularity/3.3.0
export SINGULARITY_DIR:=$(CURDIR)/$(VAR)
export SINGULARITY_IMG:=$(VAR).sif
export SINGULARITY_DEF:=$(VAR).def
singularity-build-docker:
	docker run \
	--privileged \
	--rm \
	-ti \
	-v "$(SINGULARITY_DIR):/image" "$(SINGULARITY_DOCKERTAG)" \
	bash -c ' \
	cd /image && singularity build $(SINGULARITY_IMG) $(SINGULARITY_DEF)'

singularity-build:
	cd "$(SINGULARITY_DIR)" && \
	sudo -E singularity build "$(SINGULARITY_IMG)" "$(SINGULARITY_DEF)"
