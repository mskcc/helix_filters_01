FROM continuumio/miniconda3:4.5.4

ADD bin /opt/bin
ENV PATH=/opt/bin:$PATH
