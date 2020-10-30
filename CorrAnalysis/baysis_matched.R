library(psych)
library(readr)
library(xtable)

path = "data/BAYSIS/02_matched/"
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
##### SpatAvg #####
kruskal.test(encoded$Kat~encoded$SpatAvg)
pairwise.wilcox.test(encoded$SpatAvg,encoded$Kat, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatAvg,encoded$Kat)
##### TempDist #####
kruskal.test(encoded$Kat~encoded$TempDist)
pairwise.wilcox.test(encoded$TempDist,encoded$Kat, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempDist,encoded$Kat)

sink()

###############
##### Typ #####
###############

sink(paste(path,"rstudio/Typ.txt",sep = ""))

##### SpatAvg #####
kruskal.test(encoded$Typ~encoded$SpatAvg)
pairwise.wilcox.test(encoded$SpatAvg,encoded$Typ, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatAvg,encoded$Typ)
##### TempDist #####
kruskal.test(encoded$Typ~encoded$TempDist)
pairwise.wilcox.test(encoded$TempDist,encoded$Typ, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempDist,encoded$Typ)
##### Coverage #####
kruskal.test(encoded$Typ~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$Typ, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$Typ)

sink()

#################
##### UArt1 #####
#################

sink(paste(path,"rstudio/UArt1.txt",sep = ""))

##### SpatAvg #####
kruskal.test(encoded$UArt1~encoded$SpatAvg)
pairwise.wilcox.test(encoded$SpatAvg,encoded$UArt1, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatAvg,encoded$UArt1)
##### TempDist #####
kruskal.test(encoded$UArt1~encoded$TempDist)
pairwise.wilcox.test(encoded$TempDist,encoded$UArt1, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempDist,encoded$UArt1)
##### Coverage #####
kruskal.test(encoded$UArt1~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$UArt1, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$UArt1)

sink()

#################
##### AUrs1 #####
#################

sink(paste(path,"rstudio/AUrs1.txt",sep = ""))

##### SpatAvg #####
kruskal.test(encoded$AUrs1~encoded$SpatAvg)
pairwise.wilcox.test(encoded$SpatAvg,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatAvg,encoded$AUrs1)
##### TempDist #####
kruskal.test(encoded$AUrs1~encoded$TempDist)
pairwise.wilcox.test(encoded$TempDist,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempDist,encoded$AUrs1)
##### SpatDist #####
kruskal.test(encoded$AUrs1~encoded$SpatDist)
pairwise.wilcox.test(encoded$SpatDist,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
describeBy(encoded$SpatDist,encoded$AUrs1)
##### Coverage #####
kruskal.test(encoded$AUrs1~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$AUrs1)
##### TLHGV #####
kruskal.test(encoded$AUrs1~encoded$TLHGV)
pairwise.wilcox.test(encoded$TLHGV,encoded$AUrs1, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TLHGV,encoded$AUrs1)

sink()

#################
##### AufHi #####
#################

sink(paste(path,"rstudio/AufHi.txt",sep = ""))

##### TempMax #####
kruskal.test(encoded$AufHi~encoded$TempMax)
pairwise.wilcox.test(encoded$TempMax,encoded$AufHi, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempMax,encoded$AufHi)
##### TempAvg #####
kruskal.test(encoded$AufHi~encoded$TempAvg)
pairwise.wilcox.test(encoded$TempAvg,encoded$AufHi, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempAvg,encoded$AufHi)
##### TempDist #####
kruskal.test(encoded$AufHi~encoded$TempDist)
pairwise.wilcox.test(encoded$TempDist,encoded$AufHi, paired = FALSE, p.adjust = "holm")
describeBy(encoded$TempDist,encoded$AufHi)
##### Coverage #####
kruskal.test(encoded$AufHi~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$AufHi, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$AufHi)

sink()

#################
##### Lich1 #####
#################

sink(paste(path,"rstudio/Lich1.txt",sep = ""))

##### Coverage #####
kruskal.test(encoded$Lich1~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$Lich1, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$Lich1)

sink()

#################
##### Lich2 #####
#################

sink(paste(path,"rstudio/Lich2.txt",sep = ""))

##### Coverage #####
kruskal.test(encoded$Lich2~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$Lich2, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$Lich2)

sink()

#################
##### Zust1 #####
#################

sink(paste(path,"rstudio/Zust1.txt",sep = ""))

##### Coverage #####
kruskal.test(encoded$Zust1~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$Zust1, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$Zust1)

sink()

#################
##### WoTag #####
#################

sink(paste(path,"rstudio/Month.txt",sep = ""))

##### Coverage #####
kruskal.test(encoded$WoTag~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$WoTag, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$WoTag)

sink()

#################
##### Month #####
#################

sink(paste(path,"rstudio/Month.txt",sep = ""))

##### Coverage #####
kruskal.test(encoded$Month~encoded$Coverage)
pairwise.wilcox.test(encoded$Coverage,encoded$Month, paired = FALSE, p.adjust = "holm")
describeBy(encoded$Coverage,encoded$Month)

sink()