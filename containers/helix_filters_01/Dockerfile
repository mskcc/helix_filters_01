FROM continuumio/miniconda:4.5.4

ARG COMMIT_VERSION="master"

ENV VERSION ${COMMIT_VERSION}

RUN git clone https://github.com/mskcc/helix_filters_01 /usr/bin/helix_filters_01 \
    && cd /usr/bin/helix_filters_01 \
    && git checkout $VERSION
