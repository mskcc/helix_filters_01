# NOTE: This container build NO LONGER WORKS; silent errors are encountered when installing R packages, R is no longer able to locate some compatible packages versions and results in a container that lacks some required pacakges such as 'stringr'
# This container will be un-reproducible until some method is developed to install the correct packages with version-labels (e.g. conda)
# see included packages.txt for list of R library versions from working version of this container

# To test if the container build works;
# $ docker run --rm -ti "mskcc/helix_filters_01:facets-1.6.3" Rscript -e 'library("stringr")'
# Error in library("stringr") : there is no package called ‘stringr’
# Execution halted

# NOTE: updated version of this container is here: https://github.com/mskcc/roslin-variant/blob/2.6.x/build/containers/facets/1.6.3/Dockerfile ; includes new library install scripts

FROM alpine:3.8
# copied from https://github.com/mskcc/roslin-variant/blob/2d0f7f7b78b89bb31f5bf8b8eb678fd41998213b/build/containers/facets/1.6.3/
LABEL maintainer="Nikhil Kumar (kumarn1@mskcc.org)" \
      version.image="1.0.0" \
      version.facets_suite="1.6.3" \
      version.facets="0.5.14"\
      version.alpine="3.8" \
      version.r="3.5.1" \
      version.pctGCdata="0.2.0" \
      source.facets_suite="https://github.com/mskcc/facets-suite/releases/tag/1.6.3" \
      source.facets="https://github.com/mskcc/facets/archive/v0.5.14.tar.gz"\
      source.r="https://pkgs.alpinelinux.org/package/edge/community/x86/R"

ENV FACETS_SUITE_VERSION 1.6.3
ENV FACETS_VERSION 0.5.14
ENV PCTGCDATA 0.2.0

# copy script that installs R packages
COPY install-packages.R /tmp/install-packages.R
COPY runscript.sh /usr/bin/runscript.sh
COPY run_test.sh /run_test.sh

RUN apk add --update \
        && apk add bash \
    # for wget
        && apk add ca-certificates openssl \
    # for compilation
        && apk add build-base musl-dev python py-pip python-dev \
    # install cairo and R package system dependencies
        && apk add cairo cairo-dev libxt-dev libxml2-dev font-xfree86-type1 msttcorefonts-installer \
        # configure the installed fonts
        && update-ms-fonts \
        && fc-cache -f \
    # download and install R
        && apk add R R-dev \
    # download and unzip facets, facets-suite, pctGCdata
        && cd /tmp \
        # download Facets
            && wget https://github.com/mskcc/facets/archive/v${FACETS_VERSION}.tar.gz \
        # download pctGCdata
            && wget https://github.com/mskcc/pctGCdata/archive/v${PCTGCDATA}.tar.gz \
        # download Facets_suite
            && wget https://github.com/mskcc/facets-suite/archive/${FACETS_SUITE_VERSION}.tar.gz \
        # unpack Facets
            && tar xvzf v${FACETS_VERSION}.tar.gz \
        # unpack pctGCdata
            && tar xvzf v${PCTGCDATA}.tar.gz \
        # unpack Facets_Suite
            && tar xvzf ${FACETS_SUITE_VERSION}.tar.gz \
    # install
        # install pctGCdata
            && cd /tmp/pctGCdata-${PCTGCDATA} \
            && R CMD INSTALL . \
        # install Facets
            && cd /tmp/facets-${FACETS_VERSION} \
            && R CMD INSTALL . \
        # install Facets-Suite R dependencies
            && cd /tmp \
            && Rscript --vanilla install-packages.R \
        # install Facets-Suite
            && cd /tmp/facets-suite-${FACETS_SUITE_VERSION} \
            # correct shebang line
                && sed -i "s/# parser/parser/g" geneLevel.R \
                && sed -i "s/opt\/common\/CentOS_6-dev\/R\/R-3.2.2\//usr\//g" *.R \
                && sed -i "s/opt\/common\/CentOS_6-dev\/R\/R-3.4.1\//usr\//g" *.R \
                && sed -i "s/opt\/common\/CentOS_6-dev\/R\/R-3.1.3\//usr\//g" *.R \
                && sed -i "s/opt\/common\/CentOS_6-dev\/python\/python-2.7.10\/bin\/python/usr\/bin\/env python/g" facets \
                && sed -i "s/opt\/common\/CentOS_6-dev\/bin\/current\/python/usr\/bin\/env python/g" summarize_project.py \
            # copy execs to /usr/bin/facets-suite
                && mkdir -p /usr/bin/facets-suite/ \
                && cp -r /tmp/facets-suite-${FACETS_SUITE_VERSION}/* /usr/bin/facets-suite/ \
    # clean up
        && rm -rf /var/cache/apk/* /tmp/* \
        && chmod +x /usr/bin/runscript.sh \
        && exec /run_test.sh

ENV PYTHONNOUSERSITE set
ENV FACETS_OVERRIDE_EXITCODE set
ENV LANG C.UTF-8
RUN apk add bash
