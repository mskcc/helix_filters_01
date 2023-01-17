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

    sampleData=read_tsv(file.path(pdir,"data_clinical_sample.txt"),comment="#") %>%
        left_join(dpt,by="PATIENT_ID")
    sampleData=tibble_to_named_list(sampleData,"SAMPLE_ID")

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