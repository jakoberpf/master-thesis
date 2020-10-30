library(psych)
library(readr)
library(xtable)

path = "data/ArbIS/02_matched/"
encoded <- read_delim(paste(path,"csv/encoded.csv",sep = ""), ";", escape_double = FALSE, trim_ws = TRUE)

options(xtable.floating = FALSE)
options(xtable.timestamp = "")

###################
##### Strasse #####
###################

sink(paste(path,"rstudio/Strasse.txt",sep = ""))

##### TempMax #####
kruskal.test(encoded$Strasse~encoded$TempMax)
pairwise.wilcox.test(encoded$TempMax,encoded$Strasse, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempMax,encoded$Strasse)
##### TempAvg #####
kruskal.test(encoded$Strasse~encoded$TempAvg)
pairwise.wilcox.test(encoded$TempAvg,encoded$Strasse, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempAvg,encoded$Strasse)
##### SpatMax #####
kruskal.test(encoded$Strasse~encoded$SpatMax)
pairwise.wilcox.test(encoded$SpatMax,encoded$Strasse, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatMax,encoded$Strasse)
##### SpatAvg #####
kruskal.test(encoded$Strasse~encoded$SpatAvg)
pairwise.wilcox.test(encoded$SpatAvg,encoded$Strasse, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatAvg,encoded$Strasse)
##### TempDist #####
kruskal.test(encoded$Strasse~encoded$TempDist)
pairwise.wilcox.test(encoded$TempDist,encoded$Strasse, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempDist,encoded$Strasse)
##### SpatDist #####
kruskal.test(encoded$Strasse~encoded$SpatDist)
pairwise.wilcox.test(encoded$SpatDist,encoded$Strasse, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatDist,encoded$Strasse)
##### Coverage #####
kruskal.test(encoded$Strasse~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$Strasse, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$Strasse)
##### TLCar #####
kruskal.test(encoded$Strasse~encoded$TLCar)
pairwise.wilcox.test(encoded$TLCar,encoded$Strasse, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TLCar,encoded$Strasse)
##### TLHGV #####
kruskal.test(encoded$Strasse~encoded$TLHGV)
pairwise.wilcox.test(encoded$TLHGV,encoded$Strasse, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TLHGV,encoded$Strasse)

sink()

#################
##### Month #####
#################

sink(paste(path,"rstudio/Month.txt",sep = ""))

##### TempAvg #####
kruskal.test(encoded$Month~encoded$TempAvg)
pairwise.wilcox.test(encoded$TempAvg,encoded$Month, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempAvg,encoded$Month)
##### SpatMax #####
kruskal.test(encoded$Month~encoded$SpatMax)
pairwise.wilcox.test(encoded$SpatMax,encoded$Month, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatMax,encoded$Month)
##### SpatAvg #####
kruskal.test(encoded$Month~encoded$SpatAvg)
pairwise.wilcox.test(encoded$SpatAvg,encoded$Month, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatAvg,encoded$Month)
##### TempDist #####
kruskal.test(encoded$Month~encoded$TempDist)
pairwise.wilcox.test(encoded$TempDist,encoded$Month, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempDist,encoded$Month)
##### SpatDist #####
kruskal.test(encoded$Month~encoded$SpatDist)
pairwise.wilcox.test(encoded$SpatDist,encoded$Month, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatDist,encoded$Month)
##### Coverage #####
kruskal.test(encoded$Month~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$Month, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$Month)
##### TLCar #####
kruskal.test(encoded$Month~encoded$TLCar)
pairwise.wilcox.test(encoded$TLCar,encoded$Month, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TLCar,encoded$Month)

sink()