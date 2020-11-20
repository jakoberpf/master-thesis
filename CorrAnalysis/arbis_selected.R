library(psych)
library(readr)
library(xtable)

path = "data/ArbIS/03_selected/"
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

list <- c("TempMax","TempAvg","SpatMax","SpatAvg","TempDist","SpatDist","Coverage","TLCar","TLHGV")
runAnalysis(paste(path,"rstudio/Strasse.txt",sep = ""), "Strasse", list)

#################
##### Month #####
#################

list <- c("TempAvg","SpatMax","SpatAvg","TempDist","SpatDist","Coverage","TLCar")
runAnalysis(paste(path,"rstudio/Month.txt",sep = ""), "Month", list)