# replicate continuumio/miniconda3:4.5.4 but need to install everything in a different location because /opt is not available for us
FROM debian:stretch
# https://hub.docker.com/r/continuumio/miniconda3/dockerfile
# they use 'debian:latest' which is currently 'buster' but the old container was built when 'stretch' was latest so use that instead

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

ENV PATH /usr/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.continuum.io/miniconda/Miniconda3-4.5.4-Linux-x86_64.sh -O ~/miniconda.sh && \
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

# add helix_filters files
RUN mkdir -p /usr/scripts
ADD bin /usr/scripts
ENV PATH=/usr/scripts:$PATH
