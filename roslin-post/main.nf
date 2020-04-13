// import groovy.json.JsonSlurper;
// def jsonSlurper = new JsonSlurper()
// params.roslin_resources = "roslin_resources.json"
// load the resources JSON for reference files
// def roslin_resources
// String roslin_resourcesJSON = new File("${params.roslin_resources}").text
// roslin_resources = jsonSlurper.parseText(roslin_resourcesJSON)

// python roslin_analysis_helper.py --facets_directory test_input_data/facets --inputs temp_inputs.yaml --log_directory test_input_data/log --results_directory test_input_data/ --output_directory test_input_data/ --maf_directory test_input_data/maf --sample_summary octad_inputs/Proj_OCTAD_SampleSummary.txt --clinical_data octad_inputs/Proj_OCTAD_sample_data_clinical.txt

// $ cat temp_inputs.yaml
// meta: {Assay: '', PI: '', ProjectDesc: '', ProjectID: request_id_goes_here, ProjectTitle: request_id_goes_here,
//   TumorType: ''}

// /juno/work/ci/roslin-pipelines/core/2.1.2/config/settings.sh
// /juno/work/ci/roslin-pipelines/core/2.1.2/config/variant/2.5.7/settings.sh
// /juno/work/ci/roslin-pipelines/variant/2.5.7/bin/scripts/roslin_resources.json

// /juno/work/ci/roslin-pipelines/variant/2.5.7/bin/img/facets/1.6.3/facets.sif
// !!! Uses alpine Linux; no bash; cant use with Nextflow !!
// https://github.com/mskcc/roslin-variant/blob/2.6.x/build/containers/facets/1.6.3/Dockerfile

// available command line arguments
params.outputDir = "output"
params.outputPortalDir = "${params.outputDir}/portal"
params.outputAnalysisDir = "${params.outputDir}/analysis"
params.assay = null
params.targets = null
params.pi = ''
params.project_id = 'ProjectID_1'
params.project_title = 'ProjectTitle_1'
params.tumor_type = ''
params.version = '2.x'
params.is_impact = "" //"True"
params.inputDir = 'input'
params.maf_directory = "${params.inputDir}/maf"
params.facets_directory = "${params.inputDir}/facets"

// globals
def targetsList
def targets = [
AgilentExon_51MB_b37_v3: "/juno/work/ci/resources/roslin_resources/targets/AgilentExon_51MB_b37_v3/b37/AgilentExon_51MB_b37_v3_targets.intervals",
IDT_Exome_v1_FP_b37: "/juno/work/ci/resources/roslin_resources/targets/IDT_Exome_v1_FP/b37/IDT_Exome_v1_FP_b37_targets.ilist",
E90_NimbleGeneV3_WES: "/juno/work/ci/resources/roslin_resources/targets/E90_NimbleGeneV3_WES/b37/E90_NimbleGeneV3_WES_b37_targets.ilist",
IMPACT341_b37: "/juno/work/ci/resources/roslin_resources/targets/IMPACT341/b37/picard_targets.interval_list",
IMPACT410_b37: "/juno/work/ci/resources/roslin_resources/targets/IMPACT410/b37/picard_targets.interval_list",
IMPACT468_b37: "/juno/work/ci/resources/roslin_resources/targets/IMPACT468/b37/picard_targets.interval_list",
IMPACT468_b37_mm10: "/juno/work/ci/resources/genomes/GRCh37_mm10/targets/picard_targets.interval_list",
IMPACT505: "/juno/work/ci/resources/roslin_resources/targets/IMPACT505/b37/IMPACT505_b37_targets.ilist",
IMPACT468_08390: "/juno/work/ci/resources/roslin_resources/targets/IMPACT468_08390/b37/IMPACT468_08390_b37_targets.ilist",
IMPACT468_08050: "/juno/work/ci/resources/roslin_resources/targets/IMPACT468_08050/b37/IMPACT468_08050_b37_targets.ilist",
IMPACT468_08954: "/juno/work/ci/resources/roslin_resources/targets/IMPACT468_08954/b37/IMPACT468_08954_b37_targets.ilist",
Agilent_v4_51MB_Human: "/juno/work/ci/resources/roslin_resources/targets/Agilent_v4_51MB_Human/b37/Agilent_v4_51MB_Human_b37_targets.ilist",
AgilentExon_v2: "/juno/work/ci/resources/roslin_resources/targets/AgilentExon_v2/b37/AgilentExon_v2_b37_targets.ilist",
AgilentExon_v5: "/juno/work/ci/resources/roslin_resources/targets/AgilentExon_v5/b37/AgilentExon_v5_b37_targets.ilist",
IlluminaExome_38MB: "/juno/work/ci/resources/roslin_resources/targets/IlluminaExome_38MB/b37/IlluminaExome_38MB_b37_targets.ilist",
SeqCap_EZ_Exome_v3: "/juno/work/ci/resources/roslin_resources/targets/SeqCap_EZ_Exome_v3/b37/SeqCap_EZ_Exome_v3_b37_targets.ilist",
HemePACT_v3: "/juno/work/ci/resources/roslin_resources/targets/HemePACT_v3/b37/HemePACT_v3_b37_targets.ilist",
HemePACT_v4: "/juno/work/ci/resources/roslin_resources/targets/HemePACT_v4/b37/HemePACT_v4_b37_targets.ilist"
]

if (! targets.containsKey(params.targets)){
    log.error("Value '${params.targets}' is not a registered value for 'targets'")
    log.error("Choose one of these: ${targets.keySet()}")
    exit 1
}

targetsList = targets[params.targets]

log.info("\n")
log.info("Rosling Post Processing Workflow")
log.info("targetsList: ${targetsList}")
// log.info("params: ${params}")
params.each{ k, v -> log.info("${k}: ${v}") }
log.info("\n")

targets_list = Channel.fromPath( "${targetsList}" ).first()
maf_files = Channel.fromPath( "${params.maf_directory}/*.muts.maf" )
copy_number_files = Channel.fromPath( "${params.facets_directory}/*_hisens.cncf.txt" )
segment_files = Channel.fromPath( "${params.facets_directory}/*_hisens.seg" )
segment_files.collectFile(keepHeader: true, name: "segments.combined.txt").set { combined_segments }


process generate_cbioportal_stable_ID {
    // need to check if the provided project ID is ok for use in cBioPortal (not already in use)
    // otherwise, generate a new ID. This ID will be saved in the Google Sheet for cBioPortal

    input:
    val(project_id) from "${params.project_id}"

    output:
    file("${output_file}") into cbioportal_stable_ID_txt
    // val new File("${output_file}").withReader { it.readLine() } into cbioportal_id

    script:
    output_file = "cbioportal_stable_ID.txt"
    """
    genPortalUUID.py "${project_id}" > "${output_file}"
    """
}

// read the ID from the file
// use '.first()' to create a value channel we can read from many times
cbioportal_stable_ID_txt.map { txt ->
    // read just the first line from the file
    def line
    new File("${txt}").withReader { line = it.readLine() }
    // TODO: do we have to strip trailing newline here?
    line
}.first().set { cbioportal_id }
// TODO: consider replacing this with stdout or env process output; https://www.nextflow.io/docs/edge/process.html#output-stdout-special-file

process strip_maf_comments {
    // need to strip the '#' comment lines from the .maf files headers
    input:
    file(maf) from maf_files

    output:
    file("${output_file}") into stripped_mafs

    script:
    output_file = "${maf}".replaceFirst(/.maf$/, ".strip.maf")
    """
    grep -v '#' "${maf}" > "${output_file}"
    """
}

// merge all the maf files into a single file
stripped_mafs.collectFile(keepHeader: true, name: "data_mutations_extended.combined.txt").set { combined_maf }

process filter_maf {
    // filter the maf file contents
    // this will create two filtered output files
    publishDir "${params.outputPortalDir}", mode: 'copy', pattern: "${portal_file}"
    publishDir "${params.outputAnalysisDir}", mode: 'copy', pattern: "${analysis_mut_file}"

    input:
    file(maf) from combined_maf

    output:
    file("${analysis_mut_file}")
    file("${portal_file}")

    script:
    analysis_mut_file = "${params.project_id}.muts.maf"
    portal_file = "data_mutations_extended.txt"
    """
    maf_filter.py "${maf}" "${params.version}" "${params.is_impact}" "${analysis_mut_file}" "${portal_file}"
    """
}

process fix_segment_file {
    // need to adjust the number of significant figures in the decimal place for the segment file
    publishDir "${params.outputPortalDir}", mode: 'copy', pattern: "${segmented_data_file}"
    publishDir "${params.outputAnalysisDir}", mode: 'copy', pattern: "${analysis_seg_file}"

    input:
    file(segments) from combined_segments
    val(cbio_id) from cbioportal_id

    output:
    file("${segmented_data_file}")
    file("${analysis_seg_file}")

    script:
    segmented_data_file = "${cbio_id}_data_cna_hg19.seg"
    analysis_seg_file = "${params.project_id}.seg.cna.txt"
    """
    # print out the file with fewer digits after the decimal in the seg.mean column
    python -c "
    import csv, sys;
    reader = csv.DictReader(open('${segments}'), delimiter = '\t');
    writer = csv.DictWriter(sys.stdout, fieldnames = reader.fieldnames, delimiter = '\t')
    writer.writeheader()
    for row in reader:
    \trow['seg.mean'] = '%.4f'%float(row['seg.mean'])
    \twriter.writerow(row)
    " > "${segmented_data_file}"

    # make a copy of the file with a different name for cBio portal to use
    cp "${segmented_data_file}" "${analysis_seg_file}"
    """
}


process generate_discrete_copy_number_data {
    publishDir "${params.outputPortalDir}", mode: 'copy', pattern: "${portal_CNA_file}"
    publishDir "${params.outputAnalysisDir}", mode: 'copy', pattern: "${analysis_gene_cna_file}"

    input:
    file(items: "*") from copy_number_files.collect()
    file(targets_list_file) from targets_list

    output:
    file("${portal_CNA_file}")
    file("${analysis_gene_cna_file}")

    script:
    portal_CNA_file = 'data_CNA.txt'
    analysis_gene_cna_file ="${params.project_id}.gene.cna.txt"
    """
    python /usr/bin/facets-suite/facets geneLevel \
    -o "${portal_CNA_file}" \
    --cnaMatrix \
    -f ${items} \
    --targetFile "${targets_list_file}"

    cp "${portal_CNA_file}" "${analysis_gene_cna_file}"
    """
}
