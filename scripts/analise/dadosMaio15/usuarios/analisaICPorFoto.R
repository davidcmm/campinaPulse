#!/bin/Rscript
# Calculates the confidence interval of qscores for each city point for each of the groups received

library(ggplot2)

#Calculates the variance that should be added or removed from the mean
ic <- function(x) { 
	return (sd(x)/sqrt(length(x))*qt(.95,999))#95% confidence interval for a sample of 1000 items
}

# Multiple plot function
#
# ggplot objects can be passed in ..., or to plotlist (as a list of ggplot objects)
# - cols:   Number of columns in layout
# - layout: A matrix specifying the layout. If present, 'cols' is ignored.
#
# If the layout is something like matrix(c(1,2,3,3), nrow=2, byrow=TRUE),
# then plot 1 will go in the upper left, 2 will go in the upper right, and
# 3 will go all the way across the bottom.
#
multiplot <- function(..., plotlist=NULL, file, cols=1, layout=NULL) {
  library(grid)

  # Make a list from the ... arguments and plotlist
  plots <- c(list(...), plotlist)

  numPlots = length(plots)

  # If layout is NULL, then use 'cols' to determine layout
  if (is.null(layout)) {
    # Make the panel
    # ncol: Number of columns of plots
    # nrow: Number of rows needed, calculated from # of cols
    layout <- matrix(seq(1, cols * ceiling(numPlots/cols)),
                    ncol = cols, nrow = ceiling(numPlots/cols))
  }

 if (numPlots==1) {
    print(plots[[1]])

  } else {
    # Set up the page
    grid.newpage()
    pushViewport(viewport(layout = grid.layout(nrow(layout), ncol(layout))))

    # Make each plot, in the correct location
    for (i in 1:numPlots) {
      # Get the i,j matrix positions of the regions that contain this subplot
      matchidx <- as.data.frame(which(layout == i, arr.ind = TRUE))

      print(plots[[i]], vp = viewport(layout.pos.row = matchidx$row,
                                      layout.pos.col = matchidx$col))
    }
  }
}

args <- commandArgs(trailingOnly = TRUE)

data1 <- read.table(args[1])
data2 <- read.table(args[2])
type1 <- args[3]
type2 <- args[4]

#Selecting only qscores
newdata1 <- data1 [ c(4:1003) ]
newdata2 <- data2 [ c(4:1003) ]

icData1 <- apply(newdata1, 1, ic)
icData2 <- apply(newdata2, 1, ic)

temp1 <- lapply(as.character(data1$V2), function (x) strsplit(x, split="/", fixed=TRUE)[[1]][6])
temp2 <- lapply(as.character(data2$V2), function (x) strsplit(x, split="/", fixed=TRUE)[[1]][6])

neigs1 <- unlist(lapply(temp1, '[[', 1))
neigs2 <- unlist(lapply(temp2, '[[', 1))

#Saving data
newframe1 <- data.frame(ques=data1$V1, photo=data1$V2, mean=data1$V3, dist=icData1, inf=data1$V3-icData1, sup=data1$V3+icData1, neig=neigs1)
newframe1 <- newframe1[with(newframe1, order(photo)), ]
newframe1$type <- type1
write.table(newframe1, "teste1.txt", sep="\t", row.names=FALSE, col.names=TRUE, quote=FALSE)

newframe2 <- data.frame(ques=data2$V1, photo=data2$V2, mean=data2$V3, dist=icData2, inf=data2$V3-icData1, sup=data2$V3+icData1, neig=neigs2)
newframe2 <- newframe2[with(newframe2, order(photo)), ]
newframe2$type <- type2
write.table(newframe2, "teste2.txt", sep="\t", row.names=FALSE, col.names=TRUE, quote=FALSE)

total <- rbind(newframe1, newframe2)
size <- nrow(total)
total$photo <- 1:size
total$photo [ c((size/2+1):size) ] <- (1:(size/2))

centro <- total[total$neig == "centro",]
liberdade <- total[total$neig == "liberdade",]
catole <- total[total$neig == "catole",]

pdf(file=paste("IC", args[3], args[4], ".pdf"), paper="special")
g1 <- ggplot(centro, aes(x=photo, y=mean, colour=type, title="Centro")) + geom_errorbar(aes(ymin=inf, ymax=sup), width=1, size=2) + facet_grid(. ~ ques) + xlab("Location") + ylab("QScore")
g2 <- ggplot(liberdade, aes(x=photo, y=mean, colour=type, title="Liberdade")) + geom_errorbar(aes(ymin=inf, ymax=sup), width=1, size=2) + facet_grid(. ~ ques) + xlab("Location") + ylab("QScore")
g3 <- ggplot(catole, aes(x=photo, y=mean, colour=type, title="Catole")) + geom_errorbar(aes(ymin=inf, ymax=sup), width=1, size=2) + facet_grid(. ~ ques) + xlab("Location") + ylab("QScore")

multiplot(g1, g2, g3, cols=2)

# solt$type <- "solteiro"
# casa$type <- "casado"
# novo <- rbind(solt, casa)
# novo$photo <- 1:156 + novo$photo [c(79:156) ] <- 1:78
