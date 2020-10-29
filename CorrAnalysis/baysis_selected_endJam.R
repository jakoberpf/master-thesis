library(psych)
library(readr)
library(xtable)

path = "data/BAYSIS/03_selected_03_endJam/"
encoded <- read_delim(paste(path,"csv/encoded.csv",sep = ""), ";", escape_double = FALSE, trim_ws = TRUE)

options(xtable.floating = FALSE)
options(xtable.timestamp = "")

sink(paste(path,"rstudio/Strasse.txt",sep = ""))

kruskal.test(encoded$Strasse~encoded$TempMax)
kruskal.test(encoded$Strasse~encoded$TempAvg)
kruskal.test(encoded$Strasse~encoded$SpatMax)
kruskal.test(encoded$Strasse~encoded$SpatAvg)
kruskal.test(encoded$Strasse~encoded$TempDist)
kruskal.test(encoded$Strasse~encoded$SpatDist)
kruskal.test(encoded$Strasse~encoded$Coverage)
kruskal.test(encoded$Strasse~encoded$TLHGV)

pairwise.wilcox.test(encoded$TempMax,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatMax,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatAvg,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempDist,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatDist,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TLHGV,encoded$Strasse, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$Strasse)
describeBy(encoded$TempAvg,encoded$Strasse)
describeBy(encoded$SpatMax,encoded$Strasse)
describeBy(encoded$SpatAvg,encoded$Strasse)
describeBy(encoded$TempDist,encoded$Strasse)
describeBy(encoded$SpatDist,encoded$Strasse)
describeBy(encoded$Coverage,encoded$Strasse)
describeBy(encoded$TLHGV,encoded$Strasse)

sink()

###############
##### Kat #####
###############

sink(paste(path,"rstudio/Kat.txt",sep = ""))

kruskal.test(encoded$Kat~encoded$TempMax)
kruskal.test(encoded$Kat~encoded$SpatAvg)

pairwise.wilcox.test(encoded$TempMax,encoded$Kat, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatAvg,encoded$Kat, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$Kat)
describeBy(encoded$SpatAvg,encoded$Kat)

sink()

#################
##### UArt1 #####
#################

sink(paste(path,"rstudio/UArt1.txt",sep = ""))

kruskal.test(encoded$UArt1~encoded$TempAvg)
kruskal.test(encoded$UArt1~encoded$SpatAvg)
kruskal.test(encoded$UArt1~encoded$TempDist)
kruskal.test(encoded$UArt1~encoded$Coverage)
kruskal.test(encoded$UArt1~encoded$TLHGV)

pairwise.wilcox.test(encoded$TempAvg,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatAvg,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempDist,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TLHGV,encoded$UArt1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempAvg,encoded$UArt1)
describeBy(encoded$SpatAvg,encoded$UArt1)
describeBy(encoded$TempDist,encoded$UArt1)
describeBy(encoded$Coverage,encoded$UArt1)
describeBy(encoded$TLHGV,encoded$UArt1)

sink()

#################
##### UArt2 #####
#################

sink(paste(path,"rstudio/UArt2.txt",sep = ""))

kruskal.test(encoded$UArt2~encoded$TempDist)

pairwise.wilcox.test(encoded$TempDist,encoded$UArt2, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempDist,encoded$UArt2)

sink()

#################
##### AUrs1 #####
#################

sink(paste(path,"rstudio/AUrs1.txt",sep = ""))

kruskal.test(encoded$AUrs1~encoded$TempDist)
kruskal.test(encoded$AUrs1~encoded$SpatDist)
kruskal.test(encoded$AUrs1~encoded$Coverage)
kruskal.test(encoded$AUrs1~encoded$TLHGV)

pairwise.wilcox.test(encoded$TempDist,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatDist,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TLHGV,encoded$AUrs1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempDist,encoded$AUrs1)
describeBy(encoded$SpatDist,encoded$AUrs1)
describeBy(encoded$Coverage,encoded$AUrs1)
describeBy(encoded$TLHGV,encoded$AUrs1)

sink()

#################
##### AufHi #####
#################

sink(paste(path,"rstudio/AufHi.txt",sep = ""))

kruskal.test(encoded$AufHi~encoded$TempMax)
kruskal.test(encoded$AufHi~encoded$TempAvg)
kruskal.test(encoded$AufHi~encoded$Coverage)

pairwise.wilcox.test(encoded$TempMax,encoded$AufHi, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$AufHi, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$AufHi, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$AufHi)
describeBy(encoded$TempAvg,encoded$AufHi)
describeBy(encoded$Coverage,encoded$AufHi)

sink()

#################
##### Lich1 #####
#################

sink(paste(path,"rstudio/Lich1.txt",sep = ""))

kruskal.test(encoded$Lich1~encoded$Coverage)

pairwise.wilcox.test(encoded$Coverage,encoded$Lich1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$Coverage,encoded$Lich1)

sink()

#################
##### WoTag #####
#################

sink(paste(path,"rstudio/WoTag.txt",sep = ""))

kruskal.test(encoded$WoTag~encoded$TempAvg)
kruskal.test(encoded$WoTag~encoded$SpatMax)
kruskal.test(encoded$WoTag~encoded$SpatAvg)
kruskal.test(encoded$WoTag~encoded$TempDist)
kruskal.test(encoded$WoTag~encoded$Coverage)
kruskal.test(encoded$WoTag~encoded$TLHGV)

pairwise.wilcox.test(encoded$TempAvg,encoded$WoTag, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatMax,encoded$WoTag, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatAvg,encoded$WoTag, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempDist,encoded$WoTag, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$WoTag, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TLHGV,encoded$WoTag, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempAvg,encoded$WoTag)
describeBy(encoded$SpatMax,encoded$WoTag)
describeBy(encoded$SpatAvg,encoded$WoTag)
describeBy(encoded$TempDist,encoded$WoTag)
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
kruskal.test(encoded$Month~encoded$Coverage)
kruskal.test(encoded$Month~encoded$TLHGV)

pairwise.wilcox.test(encoded$TempMax,encoded$Month, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$Month, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatMax,encoded$Month, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$Month, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TLHGV,encoded$Month, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$Month)
describeBy(encoded$TempAvg,encoded$Month)
describeBy(encoded$SpatMax,encoded$Month)
describeBy(encoded$Coverage,encoded$Month)
describeBy(encoded$TLHGV,encoded$Month)

sink()