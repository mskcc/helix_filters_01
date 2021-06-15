# version of the container from here but with bash installed ; https://github.com/mskcc/roslin-variant/blob/65d4103c7de2245923406dc95001a7e621c39dff/build/containers/getbasecountsmultisample/1.2.2/Dockerfile
FROM alpine:3.8

LABEL maintainer="Nikhil Kumar (kumarn1@mskcc.org)" \
      version.image="1.0.0" \
      version.getBaseCountsMultiSample="1.2.2" \
      version.alpine="3.8" \
      source.getBaseCountsMultiSample="https://github.com/zengzheng123/GetBaseCountsMultiSample/releases/tag/v1.2.2"

ENV GET_BASE_COUNTS_MULTI_SAMPLE_VERSION 1.2.2

COPY runscript.sh /usr/bin/runscript.sh
COPY run_test.sh /run_test.sh

RUN apk add --update \
      # for wget
            && apk add ca-certificates openssl \
      # for source compilation
            && apk add gcc g++ make cmake musl-dev zlib-dev cmake jsoncpp bash \
      # download and unzip gbcms
            && cd /tmp && wget https://github.com/zengzheng123/GetBaseCountsMultiSample/archive/v${GET_BASE_COUNTS_MULTI_SAMPLE_VERSION}.zip \
            && unzip v${GET_BASE_COUNTS_MULTI_SAMPLE_VERSION}.zip \
      # build and install bamtools
            && cd /tmp/GetBaseCountsMultiSample-${GET_BASE_COUNTS_MULTI_SAMPLE_VERSION}/bamtools-master \
            && rm -r build/ \
            && mkdir build \
            && cd build/ \
            && cmake -DCMAKE_CXX_FLAGS=-std=c++03 .. \
            && make \
            && make install \
      # copy libbamtools to /usr/lib/
            && cp ../lib/libbamtools.so.2.3.0 /usr/lib/ \
      # install getBaseCountsMultiSample
            && cd /tmp/GetBaseCountsMultiSample-${GET_BASE_COUNTS_MULTI_SAMPLE_VERSION} \
            && make \
      # copy bins to /usr/lib/
            && cp GetBaseCountsMultiSample /usr/bin/ \
      # clean up
            && rm -rf /var/cache/apk/* /tmp/* \
            && chmod +x /usr/bin/runscript.sh \
            && chmod +x /run_test.sh \
            && exec /run_test.sh

ENV LANG C.UTF-8
RUN apk add bash
