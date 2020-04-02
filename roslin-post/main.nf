import groovy.json.JsonSlurper;
def jsonSlurper = new JsonSlurper()

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
params.assay = ''
params.pi = 'Bob Sagat'
params.project_id = 'ProjectID_1'
params.project_title = 'ProjectTitle_1'
params.tumor_type = ''
params.version = '2.x'
params.is_impact = "" //"True"
params.maf_directory = 'test_input_data/maf'
params.facets_directory = 'test_input_data/facets'
params.roslin_resources = "roslin_resources.json"

// load the resources JSON for reference files
def roslin_resources
String roslin_resourcesJSON = new File("${params.roslin_resources}").text
roslin_resources = jsonSlurper.parseText(roslin_resourcesJSON)

maf_files = Channel.fromPath( "${params.maf_directory}/*.muts.maf" )
copy_number_files = Channel.fromPath( "${params.facets_directory}/*_hisens.cncf.txt" ) // generate_discrete_copy_number_data // need Facets container with bash
segment_files = Channel.fromPath( "${params.facets_directory}/*_hisens.seg" )


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

//  ~~~~~~~~~ TESTING STUFF HERE: ~~~~~~~~~
// cbioportal_id.subscribe { println "${it}" }

process foo {
    // echo true
    input:
    val(id) from cbioportal_id
    script:
    """
    echo "${id}"
    """
}
process bar {
    // echo true
    input:
    val(id) from cbioportal_id
    script:
    """
    echo "${id}"
    """
}
//  ~~~~~~~~~~~~~~~~~~

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


// copy_number_files
// output dir: portal_dir
// output file: 'data_CNA.txt'
// analysis_gene_cna_file = os.path.join(analysis_dir, portal_config_data['ProjectID'] + '.gene.cna.txt')


segment_files.collectFile(keepHeader: true, name: "segments.combined.txt").set { combined_segments }

process fix_segment_file {
    // need to adjust the number of significant figures in the decimal place for the segment file
    publishDir "${params.outputPortalDir}", mode: 'copy', pattern: "${segmented_data_file}"
    publishDir "${params.outputAnalysisDir}", mode: 'copy', pattern: "${analysis_seg_file}"

    input:
    set file(segments), val(cbio_id) from combined_segments.combine(cbioportal_id)

    output:
    file("${segmented_data_file}")
    file("${analysis_seg_file}")

    script:
    segmented_data_file = "${cbio_id}_data_cna_hg19.seg"
    analysis_seg_file = "${params.project_id}.seg.cna.txt"
    """
    python -c "
    import csv, sys;
    reader = csv.DictReader(open('${segments}'), delimiter = '\t');
    writer = csv.DictWriter(sys.stdout, fieldnames = reader.fieldnames, delimiter = '\t')
    writer.writeheader()
    for row in reader:
    \trow['seg.mean'] = '%.4f'%float(row['seg.mean'])
    \twriter.writerow(row)
    " > "${segmented_data_file}"

    cp "${segmented_data_file}" "${analysis_seg_file}"
    """
}
