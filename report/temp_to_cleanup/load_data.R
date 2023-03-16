source("load_argos.R")
require(glue)

#################################################################

number_of_events <- function(table) {
    table %>% filter(Gene!="") %>% nrow
}

load_data<-function(argos_dir,sampleID) {

    argos_data=load_argos(argos_dir)

    isUnMatched=argos_data[[sampleID]]$MATCH == "UnMatched"

    tbl01=get_clinical_table(argos_data,sampleID)

    mafTbl=get_maf_table(argos_data,sampleID,isUnMatched)

    cnvTbl=get_cnv_table(argos_data,sampleID)

    cnvTblFull=get_cnv_table_full(argos_data,sampleID)

    fusionTbl=get_fusion_table(argos_data,sampleID)

    nMut=number_of_events(mafTbl)
    nCNV=number_of_events(cnvTblFull)
    nFusion=number_of_events(fusionTbl)

    summaryTxt=glue("{nMut} mutations, {nCNV} copy number alterations, {nFusion} structural variant dectected")

    if(!isUnMatched) {

        msiTxt=glue("MSI Status = {MSI_STATUS}, score = {MSI_SCORE}",.envir=argos_data[[sampleID]])
        tmbTxt=glue("The estimated tumor mutation burden (TMB) for this sample is {CMO_TMB_SCORE} mutations per megabase (mt/Mb).",.envir=argos_data[[sampleID]])
        summaryTbl=tribble(
            ~Section, ~Data,
            "Summary:", summaryTxt,
            "MSI Status:", msiTxt,
            "Tumor Mutations Burden:", tmbTxt
        )

    } else {

        summaryTbl=tribble(
            ~Section, ~Data,
            "Summary:", summaryTxt,
            "Comments:", "This sample was run un-matched (against a pooled normal) so the ExAC Germline Filter was applied"
        )

    }

    runFolder=gsub(".*argos","",argos_dir) %>% gsub("/$","",.)

    reportTbl=tribble(
        ~key,~value,
        "Report:","Argos Report (version 0.9.5)",
        "Run Folder:", runFolder,
        "Data UUID:", digest::digest(argos_data[[sampleID]])
        )


    list(
        summaryTbl=summaryTbl,
        tbl01=tbl01,
        mafTbl=mafTbl,
        cnvTbl=cnvTbl,
        cnvTblFull=cnvTblFull,
        fusionTbl=fusionTbl,
        reportTbl=reportTbl
    )

}
