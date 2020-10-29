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

pairwise.wilcox.test(encoded$TempMax,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatMax,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatAvg,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempDist,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatDist,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$Strasse, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$Strasse)
describeBy(encoded$TempAvg,encoded$Strasse)
describeBy(encoded$SpatMax,encoded$Strasse)
describeBy(encoded$SpatAvg,encoded$Strasse)
describeBy(encoded$TempDist,encoded$Strasse)
describeBy(encoded$SpatDist,encoded$Strasse)
describeBy(encoded$Coverage,encoded$Strasse)

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

###############
##### Typ #####
###############

sink(paste(path,"rstudio/Typ.txt",sep = ""))

kruskal.test(encoded$Typ~encoded$TempDist)
kruskal.test(encoded$Typ~encoded$Coverage)

pairwise.wilcox.test(encoded$TempDist,encoded$Typ, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$Typ, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempDist,encoded$Typ)
describeBy(encoded$Coverage,encoded$Typ)

sink()

#################
##### UArt1 #####
#################

sink(paste(path,"rstudio/UArt1.txt",sep = ""))

kruskal.test(encoded$UArt1~encoded$SpatAvg)
kruskal.test(encoded$UArt1~encoded$TempDist)
kruskal.test(encoded$UArt1~encoded$Coverage)

pairwise.wilcox.test(encoded$SpatAvg,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempDist,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$UArt1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$SpatAvg,encoded$UArt1)
describeBy(encoded$TempDist,encoded$UArt1)
describeBy(encoded$Coverage,encoded$UArt1)

sink()

#################
##### AUrs1 #####
#################

sink(paste(path,"rstudio/AUrs1.txt",sep = ""))

kruskal.test(encoded$AUrs1~encoded$SpatAvg)
kruskal.test(encoded$AUrs1~encoded$TempDist)
kruskal.test(encoded$AUrs1~encoded$SpatDist)
kruskal.test(encoded$AUrs1~encoded$Coverage)
kruskal.test(encoded$AUrs1~encoded$TLHGV)

pairwise.wilcox.test(encoded$SpatAvg,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempDist,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatDist,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TLHGV,encoded$AUrs1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$SpatAvg,encoded$AUrs1)
describeBy(encoded$TempDist,encoded$AUrs1)
describeBy(encoded$Coverage,encoded$AUrs1)
describeBy(encoded$TLHGV,encoded$AUrs1)

sink()

#################
##### AufHi #####
#################

sink(paste(path,"rstudio/AufHi.txt",sep = ""))

kruskal.test(encoded$AufHi~encoded$TempMax)
kruskal.test(encoded$AufHi~encoded$TempAvg)
kruskal.test(encoded$AufHi~encoded$TempDist)
kruskal.test(encoded$AufHi~encoded$Coverage)

pairwise.wilcox.test(encoded$TempMax,encoded$AufHi, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$AufHi, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempDist,encoded$AufHi, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$AufHi, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$AufHi)
describeBy(encoded$TempAvg,encoded$AufHi)
describeBy(encoded$TempDist,encoded$AufHi)
describeBy(encoded$Coverage,encoded$AufHi)

sink()

#################
##### Lich1 #####
#################

sink(paste(path,"rstudio/Lich1.txt",sep = ""))

kruskal.test(encoded$Lich1~encoded$TempDist)
kruskal.test(encoded$Lich1~encoded$Coverage)

pairwise.wilcox.test(encoded$TempDist,encoded$Lich1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$Lich1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempDist,encoded$Lich1)
describeBy(encoded$Coverage,encoded$Lich1)

sink()

#################
##### Lich2 #####
#################

sink(paste(path,"rstudio/Lich2.txt",sep = ""))

kruskal.test(encoded$Lich2~encoded$TempDist)
kruskal.test(encoded$Lich2~encoded$Coverage)

pairwise.wilcox.test(encoded$TempDist,encoded$Lich2, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$Lich2, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempDist,encoded$Lich2)
describeBy(encoded$Coverage,encoded$Lich2)

sink()

#################
##### Zust1 #####
#################

sink(paste(path,"rstudio/Zust1.txt",sep = ""))

kruskal.test(encoded$Zust1~encoded$TempDist)
kruskal.test(encoded$Zust1~encoded$Coverage)

pairwise.wilcox.test(encoded$TempDist,encoded$Zust1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$Zust1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempDist,encoded$Zust1)
describeBy(encoded$Coverage,encoded$Zust1)

sink()

#################
##### WoTag #####
#################

sink(paste(path,"rstudio/WoTag.txt",sep = ""))

kruskal.test(encoded$WoTag~encoded$TempDist)
kruskal.test(encoded$WoTag~encoded$Coverage)

pairwise.wilcox.test(encoded$TempDist,encoded$WoTag, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$WoTag, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempDist,encoded$WoTag)
describeBy(encoded$Coverage,encoded$WoTag)

sink()

#################
##### Month #####
#################

sink(paste(path,"rstudio/Month.txt",sep = ""))

kruskal.test(encoded$Month~encoded$TempDist)
kruskal.test(encoded$Month~encoded$Coverage)

pairwise.wilcox.test(encoded$TempDist,encoded$Month, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$Month, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempDist,encoded$Month)
describeBy(encoded$Coverage,encoded$Month)

sink()