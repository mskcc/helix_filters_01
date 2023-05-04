load_oncokb <- function() {

    ARGOS_ANNOTATION_RESOURCES="/juno/work/ci/resources/genomic_resources/annotations/"
    oo=readRDS(last(fs::dir_ls(file.path(ARGOS_ANNOTATION_RESOURCES,"oncokb"))))

    #
    # Need this for join, Our MAF's keep Position fields as numbers
    #
    oo$dat=oo$dat %>% mutate(Start_Position=as.numeric(Start_Position),End_Position=as.numeric(End_Position))
    oo

    # oo$dat=oo$dat %>% mutate(Chromosome=as.numeric(Chromosome), Start_Position=as.numeric(Start_Position),End_Position=as.numeric(End_Position))


}

load_gene_annotations <- function() {
    readRDS("data/geneAnnotation.rds")
}

load_methods <- function() {
    readLines("data/methods.md")
}

load_glossary <- function() {
    read_csv("data/glossary.csv")
}
