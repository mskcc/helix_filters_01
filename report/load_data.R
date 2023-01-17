source("load_argos.R")

suppressPackageStartupMessages({
    library(tidyverse)
    library(htmlTable)
    library(kableExtra)
})

if(interactive() && exists("SOURCED") && SOURCED) halt(".INCLUDE")

argos_dir="data/argos/11704_Y/1.1.2/20221102_20_40_060423"
aa=load_argos(argos_dir)
samp=names(aa)[1]

geneAnnotation=readRDS("data/geneAnnotation.rds")

tbl01=read_csv("data/section01.csv")
tbl01$Value1=aa[[samp]][tbl01$Value1] %>% unlist
tbl01$Value2=aa[[samp]][tbl01$Value2] %>% unlist
tbl01$Value2['SAMPLE_ID']=gsub("s_","",tbl01$Value2['SAMPLE_ID']) %>% gsub("_","-",.)

#css.cell=c("padding-left: .25em","padding-left: 1em; padding-right: 6em;","padding-left: .25em;","padding-left: 1em;")

mafTbl=aa[[samp]]$MAF %>%
    filter(!grepl("=$",HGVSp_Short)) %>%
    mutate(`Additional Information`=paste0("MAF: ",round(100*t_var_freq,1),"%")) %>%
    mutate(Alteration=gsub("^p.","",HGVSp_Short)) %>%
    mutate(Alteration=paste0(Alteration," (",HGVSc,")")) %>%
    mutate(Location=paste("exon",gsub("/.*","",EXON))) %>%
    select(Gene=Hugo_Symbol,Type=Variant_Classification,Alteration,Location,`Additional Information`) %>%
    mutate_all(~replace(.,grepl("^NA|NA$",.) | is.na(.),""))

cnvTbl=aa[[samp]]$CNV %>%
    select(Gene=Hugo_Symbol,tcn,FACETS_CALL) %>%
    filter(tcn>5 | tcn<1) %>%
    left_join(geneAnnotation,by=c(Gene="hgnc.symbol")) %>%
    filter(gene_biotype=="protein_coding") %>%
    mutate(Type="Whole Gene",Alteration=FACETS_CALL) %>%
    mutate(Location=paste0(chrom,band)) %>%
    mutate(`Additional Information`=paste0("TCN: ",tcn)) %>%
    arrange(chrom) %>%
    select(Gene,Type,Alteration,Location,`Additional Information`)

SOURCED=T

