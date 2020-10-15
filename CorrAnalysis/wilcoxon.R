args <- commandArgs(trailingOnly = TRUE)
cat(args)

library(readr)
library(psych)

encoded <- read_csv("data/ArbIS/dataset/csv/encoded.csv")

kruskal.test(encoded$Length~encoded$Strasse)

pairwise.wilcox.test(encoded$Length,encoded$Strasse, paired = FALSE, p.adjust = "bonferroni")

describeBy(encoded$Length,encoded$Strasse)