SHELL:=/bin/bash
.ONESHELL:
UNAME:=$(shell uname)

# NOTE: need to upgrade the conda version to Go 1.18 ; not in conda at the moment
# https://go.dev/blog/go1.18
# https://go.dev/dl/go1.18.1.darwin-amd64.pkg
# https://go.dev/dl/go1.18.1.linux-amd64.tar.gz
# NOTE: ^^^ this requires macOS >12 ;  https://github.com/golang/go/issues/50855

# CONDA INSTALL METHOD TO USE ON DEV/PROD SERVERS
# ~~~~~ Install Dependencies ~~~~~ #
export PATH:=$(CURDIR)/conda/bin:$(CURDIR)/bin:$(PATH)
unexport PYTHONPATH
unexport PYTHONHOME

ifeq ($(UNAME), Darwin)
CONDASH:=Miniconda3-4.7.12-MacOSX-x86_64.sh
endif

ifeq ($(UNAME), Linux)
CONDASH:=Miniconda3-4.7.12-Linux-x86_64.sh
endif

CONDAURL:=https://repo.anaconda.com/miniconda/$(CONDASH)

conda:
	echo ">>> Setting up conda..."
	wget "$(CONDAURL)"
	bash "$(CONDASH)" -b -p conda
	rm -f "$(CONDASH)"

install: conda
	conda install -y conda-forge::go=1.17.8
