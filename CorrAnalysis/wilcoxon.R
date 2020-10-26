args <- commandArgs(trailingOnly = TRUE)
cat(args)

library(psych)
library(readr)

encoded <- read_delim("data/ArbIS/03_selected/csv/encoded.csv", 
                      ";", escape_double = FALSE, trim_ws = TRUE)
encoded <- read_delim("data/BAYSIS/03_selected_01_duringAndInsideOfJam/csv/encoded.csv", 
                      ";", escape_double = FALSE, trim_ws = TRUE)

kruskal.test(encoded$Strasse~encoded$SpatExMax)
kruskal.test(encoded$UArt1~encoded$SpatExMax)
kruskal.test(encoded$AufHi~encoded$SpatExMax)
kruskal.test(encoded$WoTag~encoded$SpatExMax)
kruskal.test(encoded$Month~encoded$SpatExMax)

# pairwise.wilcox.test(encoded$SpatExMax,encoded$Month, paired = FALSE, p.adjust = "bonferroni")
pairwise.wilcox.test(encoded$SpatExMax,encoded$Strasse, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatExMax,encoded$UArt1, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatExMax,encoded$AufHi, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatExMax,encoded$WoTag, paired = FALSE, p.adjust = "holm")
pairwise.wilcox.test(encoded$SpatExMax,encoded$Month, paired = FALSE, p.adjust = "holm")

describeBy(encoded$SpatExMax,encoded$Strasse)
describeBy(encoded$SpatExMax,encoded$Month)
