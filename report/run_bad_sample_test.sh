
#/juno/res/ci/voyager/argos/13726_B/1.1.2/20221227_22_01_223367/ -> remains no cnv after filtration
#/juno/res/ci/voyager/argos/05971_BN/1.1.2/20230109_23_29_954449/ -> multiple qc folders
#project: /juno/res/ci/voyager/argos/./08390_R/1.1.2/20230208_22_12_784560 running sample:  s_C_8DEVF4_P001_d01 No mutations   aa[[samp]]$MAF is NULL



#Rscript compile_sample_level.R --project_path /juno/res/ci/voyager/argos/13726_B/1.1.2/20221227_22_01_223367/ --geneAnnotation data/geneAnnotation.rds --sample_id s_C_VX8U4R_P002_d02 --output_file sil.html --output_dir /work/ci/vurals/mutation_report/test_area/


Rscript --vanilla compile_sample_level_test.R \
	--argosDir /juno/res/ci/voyager/argos/./08390_R/1.1.2/20230208_22_12_784560 \
	--sampleID  s_C_8DEVF4_P001_d01 \
	--output_dir /work/ci/vurals/mutation_report/test_area
	#--geneAnnotation_path data/geneAnnotation.rds 

##	--output_file sil.html \
