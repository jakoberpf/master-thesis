library(psych)
library(readr)
library(xtable)

path = "data/BAYSIS/03_selected_02_duringJam/"
encoded <- read_delim(paste(path,"csv/encoded.csv",sep = ""), ";", escape_double = FALSE, trim_ws = TRUE)

options(xtable.floating = FALSE)
options(xtable.timestamp = "")

sink(paste(path,"rstudio/Strasse.txt",sep = ""))

kruskal.test(encoded$Strasse~encoded$TempMax)
kruskal.test(encoded$Strasse~encoded$TempAvg)
kruskal.test(encoded$Strasse~encoded$SpatMax)
kruskal.test(encoded$Strasse~encoded$SpatAvg)
kruskal.test(encoded$Strasse~encoded$Coverage)
kruskal.test(encoded$Strasse~encoded$TLHGV)

pairwise.wilcox.test(encoded$TempMax,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatMax,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatAvg,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TLHGV,encoded$Strasse, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$Strasse)
describeBy(encoded$TempAvg,encoded$Strasse)
describeBy(encoded$SpatMax,encoded$Strasse)
describeBy(encoded$SpatAvg,encoded$Strasse)
describeBy(encoded$Coverage,encoded$Strasse)
describeBy(encoded$TLHGV,encoded$Strasse)

sink()

###############
##### Kat #####
###############

sink(paste(path,"rstudio/Kat.txt",sep = ""))

kruskal.test(encoded$Kat~encoded$TempMax)
kruskal.test(encoded$Kat~encoded$TempAvg)
kruskal.test(encoded$Kat~encoded$SpatMax)

pairwise.wilcox.test(encoded$TempMax,encoded$Kat, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$Kat, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatMax,encoded$Kat, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$Kat)
describeBy(encoded$TempAvg,encoded$Kat)
describeBy(encoded$SpatMax,encoded$Kat)

sink()

#################
##### UArt1 #####
#################

sink(paste(path,"rstudio/UArt1.txt",sep = ""))

kruskal.test(encoded$UArt1~encoded$SpatAvg)

pairwise.wilcox.test(encoded$SpatAvg,encoded$UArt1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$SpatAvg,encoded$UArt1)

sink()

#################
##### UArt2 #####
#################

sink(paste(path,"rstudio/UArt2.txt",sep = ""))

kruskal.test(encoded$UArt2~encoded$SpatMax)

pairwise.wilcox.test(encoded$SpatMax,encoded$UArt2, paired = FALSE, p.adjust = "holm")

describeBy(encoded$SpatMax,encoded$UArt2)

sink()

#################
##### AufHi #####
#################

sink(paste(path,"rstudio/AufHi.txt",sep = ""))

kruskal.test(encoded$AufHi~encoded$TempMax)
kruskal.test(encoded$AufHi~encoded$TempAvg)

pairwise.wilcox.test(encoded$TempMax,encoded$AufHi, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$AufHi, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$AufHi)
describeBy(encoded$TempAvg,encoded$AufHi)

sink()

#################
##### WoTag #####
#################

sink(paste(path,"rstudio/WoTag.txt",sep = ""))

kruskal.test(encoded$WoTag~encoded$TempAvg)
kruskal.test(encoded$WoTag~encoded$SpatMax)
kruskal.test(encoded$WoTag~encoded$Coverage)
kruskal.test(encoded$WoTag~encoded$TLHGV)

pairwise.wilcox.test(encoded$TempAvg,encoded$WoTag, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatMax,encoded$WoTag, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$WoTag, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TLHGV,encoded$WoTag, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempAvg,encoded$WoTag)
describeBy(encoded$SpatMax,encoded$WoTag)
describeBy(encoded$Coverage,encoded$WoTag)
describeBy(encoded$TLHGV,encoded$WoTag)

sink()

#################
##### Month #####
#################

sink(paste(path,"rstudio/Month.txt",sep = ""))

kruskal.test(encoded$Month~encoded$TempMax)
kruskal.test(encoded$Month~encoded$TempAvg)
kruskal.test(encoded$Month~encoded$SpatMax)
kruskal.test(encoded$Month~encoded$SpatAvg)
kruskal.test(encoded$Month~encoded$Coverage)
kruskal.test(encoded$Month~encoded$TLHGV)

pairwise.wilcox.test(encoded$TempMax,encoded$Month, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$Month, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatMax,encoded$Month, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatAvg,encoded$Month, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$Month, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TLHGV,encoded$Month, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$Month)
describeBy(encoded$TempAvg,encoded$Month)
describeBy(encoded$SpatMax,encoded$Month)
describeBy(encoded$SpatAvg,encoded$Month)
describeBy(encoded$Coverage,encoded$Month)
describeBy(encoded$TLHGV,encoded$Month)

sink()