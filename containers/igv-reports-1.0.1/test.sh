#!/bin/bash
# $ docker run -v $PWD/fasta:/fasta --rm -it mskcc/helix_filters_01:igv-reports-1.0.1 bash
set -x

create_report \
/igv-reports/examples/variants/variants.vcf.gz \
/fasta/GRCh38.d1.vd1.fa \
--ideogram /igv-reports/examples/variants/cytoBandIdeo.txt \
--flanking 1000 \
--info-columns GENE TISSUE TUMOR COSMIC_ID GENE SOMATIC \
--tracks \
/igv-reports/examples/variants/variants.vcf.gz \
/igv-reports/examples/variants/recalibrated.bam \
/igv-reports/examples/variants/refGene.sort.bed.gz \
--output igvjs_viewer.test.html
