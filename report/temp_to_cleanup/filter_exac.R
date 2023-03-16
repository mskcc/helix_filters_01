filter_exac<-function(maf) {

    highAF=maf %>%
        mutate(UUID=row_number()) %>%
        select(UUID,CLIN_SIG,matches("EXAC_AF")) %>%
        gather(Population,AF,matches("ExAC_AF")) %>%
        arrange(UUID) %>%
        filter(AF>0.0004) %>%
        distinct(UUID,CLIN_SIG)
    failClinVar=highAF %>%
        filter(!is.na(CLIN_SIG)) %>%
        separate_rows(CLIN_SIG,sep=",") %>%
        filter(CLIN_SIG %in% c("pathogenic","risk_factor","protective")) %>%
        distinct(UUID) %>%
        pull
    putativeGermline=setdiff(highAF %>% distinct(UUID) %>% pull,failClinVar)
    maf %>% filter( !(row_number() %in% putativeGermline) )

}
