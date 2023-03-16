suppressPackageStartupMessages({
    library(tidyverse)
    library(htmlTable)
    library(kableExtra)
})

source("filter_exac.R")

get_null_table <- function(msg) {
    tribble(
        ~Gene,~Type,~Alteration,~Location,~`Additional Information`,
        "","",msg,"",""
        )
}

get_clinical_table <- function(argosDb,sid) {

    clinTbl=read_csv("data/section01.csv")
    clinTbl$Value1=argosDb[[sid]][clinTbl$Value1] %>% unlist
    clinTbl$Value2=argosDb[[sid]][clinTbl$Value2] %>% unlist
    clinTbl$Value2['SAMPLE_ID']=gsub("s_","",clinTbl$Value2['SAMPLE_ID']) %>% gsub("_","-",.)

    clinTbl

}

get_maf_table <- function(argosDb,sid,unmatched) {

    if(is.null(argosDb[[sid]]$MAF)) {
        return(get_null_table("No mutations"))
    }

    if(!unmatched) {
        maf=argosDb[[sid]]$MAF
    } else {
        maf=filter_exac(argosDb[[sid]]$MAF)
    }

    if(!is.null(maf)) {

        maf %>%
            filter(!grepl("=$",HGVSp_Short)) %>%
            mutate(`Additional Information`=paste0("MAF: ",round(100*t_var_freq,1),"%")) %>%
            mutate(Alteration=gsub("^p.","",HGVSp_Short)) %>%
            mutate(Alteration=paste0(Alteration," (",HGVSc,")")) %>%
            mutate(Location=paste("exon",gsub("/.*","",EXON))) %>%
            select(Gene=Hugo_Symbol,Type=Variant_Classification,Alteration,Location,`Additional Information`) %>%
            mutate_all(~replace(.,grepl("^NA|NA$",.) | is.na(.),""))

    } else {

        get_null_table("No mutations")

    }

}

get_cnv_table <- function(argosDb,sid) {
    geneAnnotation=load_gene_annotations()
    if(!is.null(argosDb[[sid]]$CNV)) {
        tbl=argosDb[[sid]]$CNV %>%
                select(Gene=Hugo_Symbol,tcn,FACETS_CALL) %>%
                filter(tcn>5 | tcn<1) %>%
                left_join(geneAnnotation,by=c(Gene="hgnc.symbol")) %>%
                filter(gene_biotype=="protein_coding") %>%
                mutate(Type="Whole Gene",Alteration=FACETS_CALL) %>%
                mutate(Location=paste0(chrom,band)) %>%
                mutate(`Additional Information`=paste0("TCN: ",tcn)) %>%
                arrange(chrom) %>%
                select(Gene,Type,Alteration,Location,`Additional Information`)

        if(nrow(tbl)>0) {
            tbl
        } else {
            get_null_table("No AMP or HOMODEL events")
        }

    } else {
        get_null_table("No AMP or HOMODEL events")
    }

}

get_cnv_table_full <- function(argosDb,sid) {
    geneAnnotation=load_gene_annotations()
    if(!is.null(argosDb[[sid]]$CNV)) {
        argosDb[[sid]]$CNV %>%
            select(Gene=Hugo_Symbol,tcn,FACETS_CALL) %>%
            filter(tcn!=2) %>%
            left_join(geneAnnotation,by=c(Gene="hgnc.symbol")) %>%
            filter(gene_biotype=="protein_coding") %>%
            mutate(Type="Whole Gene",Alteration=FACETS_CALL) %>%
            mutate(Location=paste0(chrom,band)) %>%
            mutate(`Additional Information`=paste0("TCN: ",tcn)) %>%
            arrange(chrom) %>%
            select(Gene,Type,Alteration,Location,`Additional Information`)
    } else {
        get_null_table("No copy number events")
    }
}

get_fusion_table <- function(argosDb,sid) {
    if(!is.null(argosDb[[sid]]$Fusions)) {
        argosDb[[sid]]$Fusions %>%
            mutate(`Additional Information`=paste0("Frame: ",Frame,"; Support: DNA=",DNA_support,",RNA=",RNA_support)) %>%
            separate(Fusion,c("Alteration","Type"),sep=" ") %>%
            mutate(Location="") %>%
            select(Gene=Hugo_Symbol,Type,Alteration,Location,`Additional Information`)
    } else {
        get_null_table("No fusion events")
    }

}
