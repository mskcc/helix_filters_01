#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow
doc: "
CWL workflow for generating Roslin / Argos post pipeline analysis files and cBioPortal data and metadata files

Inputs
------

The following parameters are required:

project_id
project_pi
request_pi
project_short_name
project_name
project_description
cancer_type
cancer_study_identifier
argos_version_string
is_impact
extra_pi_groups


The following filenames are required:

analysis_mutations_filename
analysis_gene_cna_filename
analysis_sv_filename
analysis_segment_cna_filename
cbio_segment_data_filename
cbio_meta_cna_segments_filename

The following filenames have default values and are optional:

cbio_mutation_data_filename
cbio_cna_data_filename
cbio_fusion_data_filename
cbio_clinical_patient_data_filename
cbio_clinical_sample_data_filename
cbio_clinical_sample_meta_filename
cbio_clinical_patient_meta_filename
cbio_meta_study_filename
cbio_meta_cna_filename
cbio_meta_fusions_filename
cbio_meta_mutations_filename
cbio_cases_all_filename
cbio_cases_cnaseq_filename
cbio_cases_cna_filename
cbio_cases_sequenced_filename

Output
------

Workflow output should look like this:

output
├── analysis
│   ├── <project_id>.gene.cna.txt
│   ├── <project_id>.muts.maf
│   ├── <project_id>.seg.cna.txt
│   └── <project_id>.svs.maf
└── portal
    ├── case_list
    │   ├── cases_all.txt
    │   ├── cases_cnaseq.txt
    │   ├── cases_cna.txt
    │   └── cases_sequenced.txt
    ├── data_clinical_patient.txt
    ├── data_clinical_sample.txt
    ├── data_CNA.ascna.txt
    ├── data_CNA.scna.txt
    ├── data_CNA.txt
    ├── data_fusions.txt
    ├── data_mutations_extended.txt
    ├── meta_clinical_patient.txt
    ├── meta_clinical_sample.txt
    ├── meta_CNA.txt
    ├── meta_fusions.txt
    ├── meta_mutations_extended.txt
    ├── meta_study.txt
    ├── <project_id>_data_cna_hg19.seg
    └── <project_id>_meta_cna_hg19_seg.txt
"

requirements:
  ScatterFeatureRequirement: {}
  StepInputExpressionRequirement: {}
  InlineJavascriptRequirement: {}
  SubworkflowFeatureRequirement: {}

inputs:
  project_id:
    type: string
    doc: "unique identifier for the project (PROJ_ID)"
  project_pi:
    type: string
    doc: "principle investigator for the project (PROJ_PI)"
  request_pi:
    type: string
    doc: "principle investigator who requested the project (REQUEST_PI)"
  project_short_name:
    type: string
    doc: "a short name for the project in cBioPortal (PROJ_SHORT_NAME)"
  project_name:
    type: string
    doc: "a formal name for the project (PROJ_NAME)"
  project_description:
    type: string
    doc: "a description of the project (PROJ_DESC)"
  cancer_type:
    type: string
    doc: "the type of cancer used in the project (CANCER_TYPE)"
  cancer_study_identifier:
    type: string
    doc: "a study identifier for the project to use in cBioPortal (CANCER_STUDY_IDENTIFIER)"
  argos_version_string:
    type: string
    doc: "the version label of Roslin / Argos used to run the project analysis (ARGOS_VERSION_STRING)"
  is_impact:
    type: string
    doc: "whether or not the project is an IMPACT project; should be the value 'True' if so, otherwise any other value means 'False' (IS_IMPACT)"
  extra_pi_groups:
    type: string[]
    default: []
    doc: "a list of other groups to be associated with the project in cBioPortal (EXTRA_PI_GROUPS)"
  analysis_segment_cna_filename:
    type: string
    doc: "(ANALYSIS_SEGMENT_CNA_FILE; <project_id>.seg.cna.txt)"
  analysis_sv_filename:
    type: string
    doc: "(ANALYSIS_SV_FILE; <project_id>.svs.maf)"
  analysis_gene_cna_filename:
    type: string
    doc: "(ANALYSIS_GENE_CNA_FILENAME; <project_id>.gene.cna.txt)"
  analysis_mutations_filename:
    type: string
    doc: "(ANALYSIS_MUTATIONS_FILENAME; <project_id>.muts.maf)"
  cbio_segment_data_filename:
    type: string
    doc: "(CBIO_SEGMENT_DATA_FILENAME; <project_id>_data_cna_hg19.seg)"
  cbio_meta_cna_segments_filename:
    type: string
    doc: "(cbio_meta_cna_segments_filename; <project_id>_meta_cna_hg19_seg.txt)"
  cbio_cases_sequenced_filename:
    type: string
    doc: "(CBIO_CASES_SEQUENCED_FILE)"
    default: cases_sequenced.txt
  cbio_cases_cna_filename:
    type: string
    default: cases_cna.txt
    doc: "(CBIO_CASES_CNA_FILE)"
  cbio_cases_cnaseq_filename:
    type: string
    default: cases_cnaseq.txt
    doc: "(CBIO_CASES_CNASEQ_FILE)"
  cbio_cases_all_filename:
    type: string
    default: cases_all.txt
    doc: "(CBIO_CASES_ALL_FILE)"
  cbio_meta_mutations_filename:
    type: string
    default: meta_mutations_extended.txt
    doc: "(CBIO_META_MUTATIONS_FILE)"
  cbio_meta_fusions_filename:
    type: string
    default: meta_fusions.txt
    doc: "(CBIO_META_FUSIONS_FILE)"
  cbio_meta_cna_filename:
    type: string
    default: meta_CNA.txt
    doc: "(CBIO_META_CNA_FILE)"
  cbio_meta_study_filename:
    type: string
    default: meta_study.txt
    doc: "(CBIO_META_STUDY_FILE)"
  cbio_clinical_patient_meta_filename:
    type: string
    default: meta_clinical_patient.txt
    doc: "(CBIO_CLINCAL_PATIENT_META_FILE)"
  cbio_clinical_sample_meta_filename:
    type: string
    default: meta_clinical_sample.txt
    doc: "(CBIO_CLINICAL_SAMPLE_META_FILE)"
  cbio_clinical_sample_data_filename:
    type: string
    default: data_clinical_sample.txt
    doc: "(CBIO_CLINICAL_SAMPLE_DATA_FILENAME)"
  cbio_clinical_patient_data_filename:
    type: string
    default: data_clinical_patient.txt
    doc: "(CBIO_CLINCIAL_PATIENT_DATA_FILENAME)"
  cbio_fusion_data_filename:
    type: string
    default: data_fusions.txt
    doc: "(CBIO_FUSION_DATA_FILENAME)"
  cbio_mutation_data_filename:
    type: string
    default: data_mutations_extended.txt
    doc: "(CBIO_MUTATION_DATA_FILENAME)"
  cbio_cna_data_filename:
    type: string
    default: data_CNA.txt
    doc: "(CBIO_CNA_DATA_FILENAME)"
  cbio_cna_ascna_data_filename:
    type: string
    default: data_CNA.ascna.txt
    doc: "(CBIO_CNA_ASCNA_DATA_FILE)"
  cbio_cna_scna_data_filename:
    type: string
    default: data_CNA.scna.txt
    doc: "(CBIO_CNA_SCNA_DATA_FILE)"
  mutation_maf_files:
    type: File[]
    doc: "analysis_mutations_filename (ANALYSIS_MUTATIONS_FILENAME) cbio_mutation_data_filename (CBIO_MUTATION_DATA_FILENAME): (MAF_DIR)/*.muts.maf"
  facets_hisens_seg_files:
    type: File[]
    doc: "cbio_segment_data_filename (CBIO_SEGMENT_DATA_FILENAME; <project_id>_data_cna_hg19.seg) analysis_segment_cna_filename (ANALYSIS_SEGMENT_CNA_FILE; <project_id>.seg.cna.txt): (FACETS_DIR)/*_hisens.seg"
  facets_hisens_cncf_files:
    type: File[]
    doc: "cbio_cna_data_filename (CBIO_CNA_DATA_FILENAME; data_CNA.txt) analysis_gene_cna_filename (ANALYSIS_GENE_CNA_FILENAME; <project_id>.gene.cna.txt): (FACETS_DIR)/*_hisens.cncf.txt"
  mutation_svs_txt_files:
    type: File[]
    doc: "cbio_fusion_data_filename (CBIO_FUSION_DATA_FILENAME; data_fusions.txt): (MAF_DIR)/*.svs.pass.vep.portal.txt"
  mutation_svs_maf_files:
    type: File[]
    doc: "analysis_sv_filename (ANALYSIS_SV_FILE; <project_id>.svs.maf): (MAF_DIR)/*.svs.pass.vep.maf"
  targets_list:
    type: File
  known_fusions_file:
    type: File
  data_clinical_file:
    type: File
  sample_summary_file:
    type: File

steps:

  # meta_clinical_sample_file; cbio_clinical_sample_meta_filename; meta_clinical_sample.txt
  generate_meta_clinical_sample:
    run: generate_cBioPortal_file.cwl
    in:
      subcommand:
        valueFrom: ${ return "meta_sample" }
      cancer_study_id: cancer_study_identifier
      sample_data_filename:  cbio_clinical_sample_data_filename # data_clinical_sample.txt
      output_filename: cbio_clinical_sample_meta_filename
    out:
      [output_file]

  # data_clinical_patient_file; cbio_clinical_patient_data_filename; data_clinical_patient.txt
  generate_data_clinical_patient:
    run: generate_cBioPortal_file.cwl
    in:
      subcommand:
        valueFrom: ${ return "patient" }
      data_clinical_file: data_clinical_file
      output_filename: cbio_clinical_patient_data_filename
    out:
      [output_file]

  # cbio_clinical_sample_data_filename; data_clinical_sample.txt
  generate_data_clinical_sample:
    run: generate_cBioPortal_file.cwl
    in:
      subcommand:
        valueFrom: ${ return "sample" }
      data_clinical_file: data_clinical_file
      sample_summary_file: sample_summary_file
      output_filename: cbio_clinical_sample_data_filename,
      project_pi: project_pi,
      request_pi: request_pi
    out:
      [output_file]









  # strip_maf:
  #   # need to remove the '#' comment lines from the maf so we can concat them cleanly later
  #   run: strip.cwl
  #   scatter: input_file
  #   in:
  #     input_file: maf_files
  #   out:
  #     [output_file]
  #
  # reduce_sig_figs_hisens_segs:
  #   # need to reduce the number of significant figures in the hisens_segs files
  #   run: reduce_sig_figs.cwl
  #   scatter: input_file
  #   in:
  #     input_file: hisens_segs
  #   out:
  #     [output_file]
  #
  # concat_hisens_segs:
  #   # concatenate all of the hisens_segs files
  #   run: concat.cwl
  #   in:
  #     input_files: reduce_sig_figs_hisens_segs/output_file
  #   out:
  #     [output_file]
  #
  # rename_concat_hisens_segs:
  #   # rename the hisens_segs concatenated table to something that cBioPortal recognizes
  #   run: cp.cwl
  #   in:
  #     input_file: concat_hisens_segs/output_file
  #     output_filename: segment_data_file
  #   out:
  #     [output_file]
  #
  # maf_filter:
  #   # filter each maf file
  #   run: maf_filter.cwl
  #   scatter: maf_file
  #   in:
  #     maf_file: strip_maf/output_file
  #     argos_version_string: argos_version_string
  #     is_impact: is_impact
  #     analyst_filename: analysis_mutations_filename
  #     portal_filename: cbio_mutation_data_filename
  #   out: [analyst_file]
  #
  # concat_maf:
  #   # concat all the maf files into a single table
  #   run: concat.cwl
  #   in:
  #     input_files: maf_filter/analyst_file
  #   out:
  #     [output_file]
  #
  # copy_number:
  #   # run some copy number analysis on the data
  #   run: copy_number.cwl
  #   in:
  #     portal_CNA_file: cbio_cna_data_filename
  #     targets_list: targets_list
  #     hisens_cncfs: hisens_cncfs
  #   out: [output_portal_CNA_file]
  #
  # copy_cna_file:
  #   # we need this extra CWL in order to run 'cp' to output a renamed version of the CNA file for cBioPortal
  #   run: cp.cwl
  #   in:
  #     input_file: copy_number/output_portal_CNA_file
  #     output_filename: analysis_gene_cna_filename
  #   out:
  #     [output_file]
  #
  # rename_analyst_file:
  #   # we need to use this extra CWL in order to run 'cp' to output a renamed version of the analysis_mutations_filename
  #   run: cp.cwl
  #   in:
  #     input_file: concat_maf/output_file
  #     output_filename: analysis_mutations_filename
  #   out:
  #     [output_file]
  #
  # make_portal_dir:
  #   # put some files into portal dir
  #   run: put_in_dir.cwl
  #   in:
  #     segment_file: rename_concat_hisens_segs/output_file
  #     portal_cna_file: copy_number/output_portal_CNA_file
  #     output_directory_name:
  #       valueFrom: ${ return "portal"; }
  #     files:
  #       valueFrom: ${return [ inputs.portal_cna_file, inputs.segment_file ]}
  #   out: [ directory ]
  #
  # make_analysis_dir:
  #   run: put_in_dir.cwl
  #   in:
  #     analyst_file: rename_analyst_file/output_file
  #     gene_cna_file: copy_cna_file/output_file
  #     output_directory_name:
  #       valueFrom: ${ return "analysis"; }
  #     files:
  #       valueFrom: ${ return [ inputs.analyst_file, inputs.gene_cna_file ]}
  #   out: [ directory ]

outputs:
  meta_clinical_sample_file:
    type: File
    outputSource: generate_meta_clinical_sample/output_file
  data_clinical_patient_file:
    type: File
    outputSource: generate_data_clinical_patient/output_file
  data_clinical_sample_file:
    type: File
    outputSource: generate_data_clinical_sample/output_file

  # portal_dir:
  #   type: Directory
  #   outputSource: make_portal_dir/directory
  # analysis_dir:
  #   type: Directory
  #   outputSource: make_analysis_dir/directory
