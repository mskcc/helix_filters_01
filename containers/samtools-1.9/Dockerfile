# dedicated container for samtools to resolve issue here: https://github.com/PacificBiosciences/pbbioconda/issues/85
FROM debian:stretch

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
RUN conda install -c bioconda samtools=1.9 openssl=1.0
# ADD environment-base.yml /environment-base.yml
# RUN conda env update -n base --file /environment-base.yml
