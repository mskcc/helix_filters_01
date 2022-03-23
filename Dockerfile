# replicate continuumio/miniconda3:4.5.4 but need to install everything in a different location because /opt is not available for us
FROM debian:stretch
# https://hub.docker.com/r/continuumio/miniconda3/dockerfile
# they use 'debian:latest' which is currently 'buster' but the old container was built when 'stretch' was latest so use that instead

# NOTE: tried to update to continuumio/miniconda3:4.10.3 but had issues described here; https://github.com/conda/conda/issues/9836
# https://github.com/ContinuumIO/docker-images/blob/cab0488275842955fa5ac6cb96ea05b316f08b3a/miniconda3/debian/Dockerfile
# https://hub.docker.com/layers/continuumio/miniconda3/4.10.3/images/sha256-59aeaac73f2d5998475c594d33241ff6f9a92f4bdc24c4a183785ba7651f339f?context=explore


ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

ENV PATH /usr/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.7.12-Linux-x86_64.sh -O ~/miniconda.sh && \
/bin/bash ~/miniconda.sh -b -p /usr/conda && \
rm ~/miniconda.sh && \
/usr/conda/bin/conda clean -tipsy && \
ln -s /usr/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
echo ". /usr/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
echo "conda activate base" >> ~/.bashrc

ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]

# install extra libraries into base env
ADD environment-base.yml /environment-base.yml
RUN conda env update -n base --file /environment-base.yml
# RUN conda list --explicit > /environment.txt

# add separate env for R; use it like this: $ docker run --rm 'my-container' conda run -n env-r --no-capture-output myscript.R args go here
# ADD environment-r.yml /environment-r.yml
# RUN conda env update -n r --file /environment-r.yml
# NOTE: don't use this due to issue using conda run from Singularity ; https://github.com/conda/conda/issues/10888

# test to make sure it works
RUN samtools --version
RUN bedtools --version
RUN vcf2maf.pl --help
RUN bedops --version

# add helix_filters files
RUN mkdir -p /usr/scripts
ENV PATH=/usr/scripts:$PATH
ADD bin /usr/scripts
