# replicate continuumio/miniconda3:4.5.4 but need to install everything in a different location because /usr is not available for us
# based on:
# https://github.com/ContinuumIO/docker-images/blob/cab0488275842955fa5ac6cb96ea05b316f08b3a/miniconda3/debian/Dockerfile
# https://hub.docker.com/layers/continuumio/miniconda3/4.10.3/images/sha256-59aeaac73f2d5998475c594d33241ff6f9a92f4bdc24c4a183785ba7651f339f?context=explore
FROM debian:buster-slim

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update -q && \
    apt-get install -q -y --no-install-recommends \
        bzip2 \
        ca-certificates \
        git \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        procps \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
# subversion mercurial openssh-client

ENV PATH /usr/conda/bin:$PATH

CMD [ "/bin/bash" ]

RUN wget "https://repo.anaconda.com/miniconda/Miniconda3-py39_4.10.3-Linux-x86_64.sh" -O miniconda.sh -q && \
    mkdir -p /usr && \
    sh miniconda.sh -b -p /usr/conda && \
    rm miniconda.sh && \
    ln -s /usr/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /usr/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /usr/conda/ -follow -type f -name '*.a' -delete && \
    find /usr/conda/ -follow -type f -name '*.js.map' -delete && \
    /usr/conda/bin/conda clean -afy

# install extra libraries
ADD environment.yml /environment.yml
RUN conda env update -n base --file /environment.yml
RUN mkdir -p /usr/report
ADD report /usr/report
ENV PATH=/usr/report:$PATH
