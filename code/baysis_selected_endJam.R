library(psych)
library(readr)
library(xtable)

path = "data/BAYSIS/03_selected_03_endJam/"
encoded <- read_delim(paste(path,"csv/encoded.csv",sep = ""), ";", escape_double = FALSE, trim_ws = TRUE)

options(xtable.floating = FALSE)
options(xtable.timestamp = "")

runAnalysis <- function(output, main, slaves) {
  sink(output)
  for (param in slaves) {
    print(paste("############",paste(param,"############",sep = " "),sep = " "))
    var.kruskal = kruskal.test(encoded[[main]]~encoded[[param]])
    print(var.kruskal)
    if (var.kruskal[["p.value"]] < 0.05) {
      var.pairwise = pairwise.wilcox.test(encoded[[param]],encoded[[main]], paired = FALSE, p.adjust = "holm")
      print(xtable(var.pairwise[["p.value"]]))
      var.describe = describeBy(encoded[[param]],encoded[[main]])
      var.merge = var.describe[[1]]
      var.merge = var.merge[FALSE,]
      for (i in 1:length(var.describe)) {
        var.merge = rbind(var.merge,var.describe[[i]])
      }
      print(xtable(var.merge))
      rm(var.pairwise,var.describe,var.merge)
    }
    rm(var.kruskal)
  }
  sink()
}

###################
##### Strasse #####
###################

list <- c("TempMax","TempAvg","SpatMax","SpatAvg","TempDist","SpatDist","Coverage","TLHGV")
runAnalysis(paste(path,"rstudio/Strasse.txt",sep = ""), "Strasse", list)

###############
##### Kat #####
###############

list <- c("TempMax","SpatAvg")
runAnalysis(paste(path,"rstudio/Kat.txt",sep = ""), "Kat", list)

#################
##### UArt1 #####
#################

list <- c("TempMax","SpatAvg","TempDist","Coverage","TLHGV")
runAnalysis(paste(path,"rstudio/UArt1.txt",sep = ""), "UArt1", list)

#################
##### UArt2 #####
#################

list <- c("TempDist")
runAnalysis(paste(path,"rstudio/UArt2.txt",sep = ""), "UArt2", list)

#################
##### AUrs1 #####
#################

list <- c("TempDist","SpatDist","Coverage","TLHGV")
runAnalysis(paste(path,"rstudio/AUrs1.txt",sep = ""), "AUrs1", list)

#################
##### AufHi #####
#################

list <- c("TempMax","TempAvg","Coverage")
runAnalysis(paste(path,"rstudio/AufHi.txt",sep = ""), "AufHi", list)

#################
##### Lich1 #####
#################

list <- c("Coverage")
runAnalysis(paste(path,"rstudio/Lich1.txt",sep = ""), "Lich1", list)

#################
##### WoTag #####
#################

list <- c("TempMax","SpatMax","SpatAvg","TempDist","Coverage","TLHGV")
runAnalysis(paste(path,"rstudio/WoTag.txt",sep = ""), "WoTag", list)

#################
##### Month #####
#################

list <- c("TempMax","TempAvg","SpatMax","Coverage","TLHGV")
runAnalysis(paste(path,"rstudio/Month.txt",sep = ""), "Month", list)