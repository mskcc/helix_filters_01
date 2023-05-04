args=commandArgs(trailing=T)

argosDir=args[1]
sampleID=args[2]

source("load_data.R")
data=load_data(argosDir,sampleID)

