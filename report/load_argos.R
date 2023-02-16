suppressPackageStartupMessages({
    library(readr)
    library(dplyr)
    library(purrr)
    library(jsonlite)
})

tibble_to_named_list<-function(tbl,col) {
    nl=transpose(tbl)
    names(nl)=map(nl,col) %>% unlist
    nl
}

get_with_default<-function(ll,key) {
    if(key %in% names(ll)) {
        return(ll[[key]])
    } else {
        return(NULL)
    }
}

load_argos<-function(odir) {

    pdir=file.path(odir,"portal")
    adir=file.path(odir,"analysis")

    dpt=read_tsv(file.path(pdir,"data_clinical_patient.txt"),comment="#")

    sampleTbl=read_tsv(file.path(pdir,"data_clinical_sample.txt"),comment="#") %>%
        left_join(dpt,by="PATIENT_ID")

    #
    # Get normal ID and add Matched status
    #

    qc_dir <- list.files(paste(odir,"json",sep="/"), pattern = "argos_qc.*",full.names = TRUE)
    json_files <- list.files(qc_dir, pattern = "input\\.json$",recursive = TRUE, full.names = TRUE)
    inputJsonFile <- json_files[which.max(file.info(json_files)$mtime)] ##most_recent_file

    if (length(inputJsonFile)== 0) {
        print("Couldn't find json file, maybe it is an old project")
        quit(status=1)
    }
    
    #inputJsonFile=fs::dir_ls(file.path(odir,"json"),recur=T,regex="argos_qc.*input\\.json$")
    inputJson=read_json(inputJsonFile)

    pairingTable=tibble(
            SAMPLE_ID=unlist(inputJson$tumor_sample_names),
            NORMAL_ID=unlist(inputJson$normal_sample_names)
        ) %>%
        mutate(NORMAL_ID=gsub("_","-",NORMAL_ID) %>% gsub("^s-","",.))

    sampleTbl=left_join(sampleTbl,pairingTable) %>%
        rowwise %>%
        mutate(MATCHED=ifelse(grepl(PATIENT_ID,NORMAL_ID),"Matched","UnMatched")) %>%
        ungroup

    sampleData=tibble_to_named_list(sampleTbl,"SAMPLE_ID")

    # maf=read_tsv(file.path(pdir,"data_mutations_extended.txt"),comment="#") %>%
    #     group_split(Tumor_Sample_Barcode)
    # names(maf)=map(maf,\(x){x$Tumor_Sample_Barcode[1]}) %>% unlist
    # pmaf=maf

    maf=read_tsv(fs::dir_ls(adir,regex=".muts.maf$"),comment="#") %>%
        group_split(Tumor_Sample_Barcode)
    names(maf)=map(maf,\(x){x$Tumor_Sample_Barcode[1]}) %>% unlist

    fusions=read_tsv(file.path(pdir,"data_fusions.txt"),comment="#") %>%
        group_split(Tumor_Sample_Barcode)
    names(fusions)=map(fusions,\(x){x$Tumor_Sample_Barcode[1]}) %>% unlist

    # cnv=read_tsv(file.path(pdir,"data_CNA.txt"),comment="#") %>%
    #     gather(Tumor_Sample_Barcode,CNV,-Hugo_Symbol) %>%
    #     filter(CNV!=0 & !is.na(CNV)) %>%
    #     group_split(Tumor_Sample_Barcode)
    # names(cnv)=map(cnv,\(x){x$Tumor_Sample_Barcode[1]}) %>% unlist

    cnv=read_tsv(fs::dir_ls(adir,regex=".gene.cna.txt"),comment="#") %>%
        mutate(Tumor_Sample_Barcode=gsub("_[^_]*$","",Tumor_Sample_Barcode)) %>%
        group_split(Tumor_Sample_Barcode)
    names(cnv)=map(cnv,\(x){x$Tumor_Sample_Barcode[1]}) %>% unlist

    for(si in names(sampleData)) {
#        sampleData[[si]]$pMAF=get_with_default(pmaf,si)
        sampleData[[si]]$MAF=get_with_default(maf,si)
        sampleData[[si]]$CNV=get_with_default(cnv,si)
        sampleData[[si]]$Fusions=get_with_default(fusions,si)
    }

    sampleData

}