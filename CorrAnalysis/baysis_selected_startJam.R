library(psych)
library(readr)
library(xtable)

path = "data/BAYSIS/03_selected_01_startJam/"
encoded <- read_delim(paste(path,"csv/encoded.csv",sep = ""), ";", escape_double = FALSE, trim_ws = TRUE)

options(xtable.floating = FALSE)
options(xtable.timestamp = "")

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
##### Coverage #####
kruskal.test(encoded$Strasse~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$Strasse, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$Strasse)
##### TLCar #####
kruskal.test(encoded$Strasse~encoded$TLCar)
pairwise.wilcox.test(encoded$TLCar,encoded$Strasse, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TLCar,encoded$Strasse)

sink()

###############
##### Kat #####
###############

sink(paste(path,"rstudio/Kat.txt",sep = ""))

##### TempMax #####
kruskal.test(encoded$Kat~encoded$TempMax)
pairwise.wilcox.test(encoded$TempMax,encoded$Kat, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempMax,encoded$Kat)
##### TempAvg #####
kruskal.test(encoded$Kat~encoded$TempAvg)
pairwise.wilcox.test(encoded$TempAvg,encoded$Kat, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempAvg,encoded$Kat)
##### SpatMax #####
kruskal.test(encoded$Kat~encoded$SpatMax)
pairwise.wilcox.test(encoded$SpatMax,encoded$Kat, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatMax,encoded$Kat)
##### SpatAvg #####
kruskal.test(encoded$Kat~encoded$SpatAvg)
pairwise.wilcox.test(encoded$SpatAvg,encoded$Kat, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatAvg,encoded$Kat)

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

kruskal.test(encoded$UArt1~encoded$TempMax)
kruskal.test(encoded$UArt1~encoded$TempAvg)
kruskal.test(encoded$UArt1~encoded$SpatMax)
kruskal.test(encoded$UArt1~encoded$SpatAvg)
kruskal.test(encoded$UArt1~encoded$TempDist)
kruskal.test(encoded$UArt1~encoded$Coverage)
kruskal.test(encoded$UArt1~encoded$TLCar)

pairwise.wilcox.test(encoded$TempMax,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatMax,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatAvg,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempDist,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TLCar,encoded$UArt1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$UArt1)
describeBy(encoded$TempAvg,encoded$UArt1)
describeBy(encoded$SpatMax,encoded$UArt1)
describeBy(encoded$SpatAvg,encoded$UArt1)
describeBy(encoded$TempDist,encoded$UArt1)
describeBy(encoded$Coverage,encoded$UArt1)
describeBy(encoded$TLCar,encoded$UArt1)

sink()

#################
##### AUrs1 #####
#################

sink(paste(path,"rstudio/AUrs1.txt",sep = ""))

kruskal.test(encoded$AUrs1~encoded$TempMax)
kruskal.test(encoded$AUrs1~encoded$TempAvg)
kruskal.test(encoded$AUrs1~encoded$SpatMax)
kruskal.test(encoded$AUrs1~encoded$SpatAvg)
kruskal.test(encoded$AUrs1~encoded$TempDist)
kruskal.test(encoded$AUrs1~encoded$Coverage)
kruskal.test(encoded$AUrs1~encoded$TLHGV)

pairwise.wilcox.test(encoded$TempMax,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatMax,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatAvg,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempDist,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$Coverage,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TLHGV,encoded$AUrs1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$AUrs1)
describeBy(encoded$TempAvg,encoded$AUrs1)
describeBy(encoded$SpatMax,encoded$AUrs1)
describeBy(encoded$SpatAvg,encoded$AUrs1)
describeBy(encoded$TempDist,encoded$AUrs1)
describeBy(encoded$Coverage,encoded$AUrs1)
describeBy(encoded$TLHGV,encoded$AUrs1)

sink()

#################
##### AUrs2 #####
#################

sink(paste(path,"rstudio/AUrs2.txt",sep = ""))

kruskal.test(encoded$AUrs2~encoded$TempMax)
kruskal.test(encoded$AUrs2~encoded$TempAvg)
kruskal.test(encoded$AUrs2~encoded$SpatAvg)
kruskal.test(encoded$AUrs2~encoded$TempDist)

pairwise.wilcox.test(encoded$TempMax,encoded$AUrs2, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempAvg,encoded$AUrs2, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatAvg,encoded$AUrs2, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$TempDist,encoded$AUrs2, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempMax,encoded$AUrs2)
describeBy(encoded$TempAvg,encoded$AUrs2)
describeBy(encoded$SpatAvg,encoded$AUrs2)
describeBy(encoded$TempDist,encoded$AUrs2)

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
##### Char1 #####
#################

sink(paste(path,"rstudio/Char1.txt",sep = ""))

kruskal.test(encoded$Char1~encoded$TempDist)

pairwise.wilcox.test(encoded$TempDist,encoded$Char1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempDist,encoded$Char1)

sink()

#################
##### Lich1 #####
#################

sink(paste(path,"rstudio/Lich1.txt",sep = ""))

kruskal.test(encoded$Lich1~encoded$TempDist)

pairwise.wilcox.test(encoded$TempDist,encoded$Lich1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempDist,encoded$Lich1)

sink()

#################
##### Lich2 #####
#################

sink(paste(path,"rstudio/Lich2.txt",sep = ""))

kruskal.test(encoded$Lich2~encoded$TempDist)

pairwise.wilcox.test(encoded$TempDist,encoded$Lich2, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempDist,encoded$Lich2)

sink()

#################
##### Zust1 #####
#################

sink(paste(path,"rstudio/Zust1.txt",sep = ""))

kruskal.test(encoded$Zust1~encoded$Coverage)

pairwise.wilcox.test(encoded$Coverage,encoded$Zust1, paired = FALSE, p.adjust = "holm")

describeBy(encoded$Coverage,encoded$Zust1)

sink()

#################
##### Zust2 #####
#################

sink(paste(path,"rstudio/Zust2.txt",sep = ""))

kruskal.test(encoded$Zust2~encoded$TempAvg)
kruskal.test(encoded$Zust2~encoded$SpatAvg)

pairwise.wilcox.test(encoded$TempAvg,encoded$Zust2, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatAvg,encoded$Zust2, paired = FALSE, p.adjust = "holm")

describeBy(encoded$TempAvg,encoded$Zust2)
describeBy(encoded$SpatAvg,encoded$Zust2)

sink()

#################
##### Month #####
#################

sink(paste(path,"rstudio/Month.txt",sep = ""))

kruskal.test(encoded$Month~encoded$Coverage)

pairwise.wilcox.test(encoded$Coverage,encoded$Month, paired = FALSE, p.adjust = "holm")

describeBy(encoded$Coverage,encoded$Month)

sink()