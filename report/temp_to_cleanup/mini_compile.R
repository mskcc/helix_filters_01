

rmarkdown::render(
    input = "report_sample_level.Rmd", 
    params = list(
        argosDir = "/juno/res/ci/voyager/argos/13726_B/1.1.2/20221227_22_01_223367",
        sampleID = "s_C_001656_M002_d02"
    ),
    output_format = "html_document",
    output_file = "report.html",
    clean = TRUE
)
