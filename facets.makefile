SHELL:=/bin/bash
.ONESHELL:

FACETS_SNPS_VCF:=/juno/work/ci/resources/genomes/GRCh37/facets_snps/dbsnp_137.b37__RmDupsClean__plusPseudo50__DROP_SORT.vcf
PROJ_ID:=Proj_08390_G
TEST_DATA_DIR:=/juno/work/ci/helix_filters_01/test_data/$(PROJ_ID)
BAM_DIR:=$(TEST_DATA_DIR)/bam
MAF_DIR:=$(TEST_DATA_DIR)/maf
PAIRING_FILE:=$(TEST_DATA_DIR)/inputs/Proj_08390_G_sample_pairing.txt
OUTPUT_DIR:=$(CURDIR)/output
CONTAINER_SIF=$(CURDIR)/facets-suite_dev.sif

$(OUTPUT_DIR):
	mkdir -p "$(OUTPUT_DIR)"

SNP_OUTPUT:=$(OUTPUT_DIR)/snp_pileup
$(SNP_OUTPUT): $(OUTPUT_DIR)
	mkdir -p $(SNP_OUTPUT)

FACETS_OUTPUT:=$(OUTPUT_DIR)/facets
$(FACETS_OUTPUT): $(OUTPUT_DIR)
	mkdir -p $(FACETS_OUTPUT)

MAF_OUTPUT:=$(OUTPUT_DIR)/maf
$(MAF_OUTPUT):
	mkdir -p $(MAF_OUTPUT)

LOG_DIR:=$(OUTPUT_DIR)/log
$(LOG_DIR):
	mkdir -p $(LOG_DIR)

# pull down and convert the Singularity container: $(CONTAINER_SIF)
pull:
	module load singularity/3.3.0
	singularity pull docker://stevekm/facets-suite:dev

# real	63m0.888s
# user	1187m25.113s
# sys	31m54.088s
PAIRS:=$(shell cat $(PAIRING_FILE) | tr '\t' ',')
$(PAIRS): $(SNP_OUTPUT) $(FACETS_OUTPUT) $(MAF_OUTPUT) $(LOG_DIR)
	tumor="$$(echo $@ | cut -d ',' -f2)"
	normal="$$(echo $@ | cut -d ',' -f1)"
	tumor_bam="$(BAM_DIR)/$$tumor.rg.md.abra.printreads.bam"
	normal_bam="$(BAM_DIR)/$$normal.rg.md.abra.printreads.bam"
	tumor_pileup="$(OUTPUT_DIR)/snp-pileup/$$tumor.snp_pileup.gz"
	normal_pileup="$(OUTPUT_DIR)/snp-pileup/$$normal.snp_pileup.gz"
	pair_id="$${tumor}.$${normal}"
	pair_maf="$(MAF_DIR)/$${pair_id}.muts.maf"
	annot_maf="$(MAF_OUTPUT)/$${pair_id}_hisens.ccf.maf"
	snp_prefix="$(SNP_OUTPUT)/$${pair_id}"
	snp_pileup="$${snp_prefix}.snp_pileup.gz"
	facets_rds="$(FACETS_OUTPUT)/$${pair_id}_hisens.rds"
	log_file="$(LOG_DIR)/$${pair_id}.log"
	(
	module load singularity/3.3.0
	set -x
	singularity exec \
	-B /juno/work \
	-B "$(CURDIR)" \
	-B "$(SNP_OUTPUT)" \
	-B /juno/work/ci/resources/genomes/GRCh37/facets_snps \
	-B "$(BAM_DIR)" \
	"$(CONTAINER_SIF)" \
	/bin/bash -c " \
	cd $(CURDIR)
	snp-pileup-wrapper.R \
	--vcf-file $(FACETS_SNPS_VCF) \
	--normal-bam $${normal_bam} \
	--tumor-bam $${tumor_bam} \
	--output-prefix "$${snp_prefix}"
	" && \
	singularity exec \
	-B /juno/work \
	-B "$(CURDIR)" \
	-B "$(FACETS_OUTPUT)" \
	"$(CONTAINER_SIF)" \
	/bin/bash -c " \
	cd $(CURDIR)
	run-facets-wrapper.R \
	--counts-file $${snp_pileup} \
	--sample-id $${pair_id} \
	--purity-cval 100 \
	--cval 50 \
	--seed 1000 \
	--everything \
	--min-nhet 25 \
	--purity-min-nhet 25 \
	-D $(FACETS_OUTPUT) \
	--facets-lib-path /usr/local/lib/R/site-library
	" && \
	singularity exec \
	-B /juno/work \
	-B "$(CURDIR)" \
	-B "$(FACETS_OUTPUT)" \
	-B "$(OUTPUT_DIR)" \
	-B "$(MAF_DIR)" \
	"$(CONTAINER_SIF)" \
	/bin/bash -c " \
	cd $(CURDIR)
	annotate-maf-wrapper.R \
	--maf-file $${pair_maf} \
	--facets-output $${facets_rds} \
	-o $${annot_maf}
	" || echo ">>> pair $${pair_id} failed a pipeline step"
	) 2>&1 | tee $${log_file}


.PHONY: $(PAIRS)
test: $(PAIRS)
# pairing:
# 	@while IFS=$$(printf '\t') read -r tumor normal; do
# 	tumor_bam="$(BAM_DIR)/$$tumor.rg.md.abra.printreads.bam"
# 	normal_bam="$(BAM_DIR)/$$normal.rg.md.abra.printreads.bam"
# 	tumor_pileup="$(OUTPUT_DIR)/snp-pileup/$$tumor.snp_pileup.gz"
# 	normal_pileup="$(OUTPUT_DIR)/snp-pileup/$$normal.snp_pileup.gz"
# 	echo "$$tumor_bam : $$tumor_pileup, $$normal_bam : $$normal_pileup"
# 	done <$(PAIRING_FILE)

SNP_PILEUP:=$(OUTPUT_DIR)/snp-pileup/s_C_ABCD_P001_d_s_C_ABCD_N001_d.snp_pileup.gz
snp-pileup:
	mkdir -p $(OUTPUT_DIR)/snp-pileup
	module load singularity/3.3.0
	singularity exec \
	-B /juno/work \
	-B "$(CURDIR)" \
	-B "$(OUTPUT_DIR)/snp-pileup" \
	-B /juno/work/ci/resources/genomes/GRCh37/facets_snps \
	-B "$(TEST_DATA_DIR)" \
	"$(CONTAINER_SIF)" \
	/bin/bash -c ' \
	cd $(CURDIR)
	snp-pileup-wrapper.R \
	--vcf-file $(FACETS_SNPS_VCF) \
	--normal-bam $(TEST_DATA_DIR)/bam/s_C_ABCD_N001_d.rg.md.abra.printreads.bam \
	--tumor-bam $(TEST_DATA_DIR)/bam/s_C_ABCD_P001_d.rg.md.abra.printreads.bam \
	--output-prefix $(OUTPUT_DIR)/snp-pileup/s_C_ABCD_P001_d_s_C_ABCD_N001_d
	'



# without --legacy-output
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_purity.seg
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_purity.png
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.seg
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.png
# s_C_ABCD_P001_d_s_C_ABCD_N001_d.qc.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d.gene_level.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d.arm_level.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_purity.rds
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.rds
run-facets:
	mkdir -p $(OUTPUT_DIR)/run-facets
	module load singularity/3.3.0
	singularity exec \
	-B /juno/work \
	-B "$(CURDIR)" \
	-B "$(OUTPUT_DIR)/run-facets" \
	"$(CONTAINER_SIF)" \
	/bin/bash -c ' \
	cd $(CURDIR)
	run-facets-wrapper.R \
	--counts-file $(SNP_PILEUP) \
	--sample-id s_C_ABCD_P001_d_s_C_ABCD_N001_d \
	--purity-cval 100 \
	--cval 50 \
	--seed 1000 \
	--everything \
	--min-nhet 25 \
	--purity-min-nhet 25 \
	-D $(OUTPUT_DIR)/run-facets \
	--facets-lib-path /usr/local/lib/R/site-library
	'

# --legacy-output TRUE
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_purity.seg
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_purity.CNCF.png
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.seg
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.CNCF.png
# s_C_ABCD_P001_d_s_C_ABCD_N001_d.qc.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d.gene_level.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d.arm_level.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.cncf.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.Rdata
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.out
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_purity.cncf.txt
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_purity.Rdata
# s_C_ABCD_P001_d_s_C_ABCD_N001_d_purity.out
run-facets-legacy:
	mkdir -p $(OUTPUT_DIR)/run-facets-legacy
	module load singularity/3.3.0
	singularity exec \
	-B /juno/work \
	-B "$(CURDIR)" \
	-B "$(OUTPUT_DIR)/run-facets-legacy" \
	"$(CONTAINER_SIF)" \
	/bin/bash -c ' \
	cd $(CURDIR)
	run-facets-wrapper.R \
	--counts-file $(SNP_PILEUP) \
	--sample-id s_C_ABCD_P001_d_s_C_ABCD_N001_d \
	--purity-cval 100 \
	--cval 50 \
	--seed 1000 \
	--everything \
	--min-nhet 25 \
	--purity-min-nhet 25 \
	-D $(OUTPUT_DIR)/run-facets-legacy \
	--facets-lib-path /usr/local/lib/R/site-library \
	--legacy-output TRUE
	'


annotate-maf:
	mkdir -p $(OUTPUT_DIR)/annotate-maf
	module load singularity/3.3.0
	singularity exec \
	-B /juno/work \
	-B "$(CURDIR)" \
	-B "$(OUTPUT_DIR)/annotate-maf" \
	-B "$(OUTPUT_DIR)/run-facets" \
	-B "$(TEST_DATA_DIR)" \
	"$(CONTAINER_SIF)" \
	/bin/bash -c ' \
	cd $(CURDIR)
	annotate-maf-wrapper.R \
	--maf-file $(TEST_DATA_DIR)/maf/s_C_ABCD_P001_d.s_C_ABCD_N001_d.muts.maf \
	--facets-output $(OUTPUT_DIR)/run-facets/s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.rds \
	-o $(OUTPUT_DIR)/annotate-maf/s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.ccf.maf
	'

# Error: Provide either a sample mapping or single-sample Facets output file.
# annotate-maf-nofacets:
# 	mkdir -p $(OUTPUT_DIR)/annotate-maf-nofacets
# 	module load singularity/3.3.0
# 	singularity exec \
# 	-B /juno/work \
# 	-B "$(CURDIR)" \
# 	-B "$(OUTPUT_DIR)/annotate-maf-nofacets" \
# 	-B "$(TEST_DATA_DIR)" \
# 	"$(CONTAINER_SIF)" \
# 	/bin/bash -c ' \
# 	cd $(CURDIR)
# 	annotate-maf-wrapper.R \
# 	--maf-file $(TEST_DATA_DIR)/maf/s_C_ABCD_P001_d.s_C_ABCD_N001_d.muts.maf \
# 	-o $(OUTPUT_DIR)/annotate-maf-nofacets/s_C_ABCD_P001_d_s_C_ABCD_N001_d_hisens.ccf.maf
# 	'



run: $(OUTPUT_DIR) snp-pileup run-facets run-facets-legacy annotate-maf

clean-all:
	rm -rf $(OUTPUT_DIR)
