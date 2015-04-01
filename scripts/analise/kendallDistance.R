# Functions to calculate the kendall tau distance of two rankings

mergeSort <- function(x){
  # Sorts a list computing the number of inversions
  #
  # Args:
  #   x: list with itens to be sorted
  # Returns:
  #   List with two values: 
  #     "inversions": number of inversions and sorted list
  #     "sortedVector": x sorted
  #
  # Method adapted from http://goo.gl/LyDFRf

  if(length(x) == 1){
    inv <- 0
  } else {
    n <- length(x)
    n1 <- ceiling(n/2)
    n2 <- n-n1
    y1 <- mergeSort(x[1:n1])
    y2 <- mergeSort(x[n1+1:n2])
    inv <- y1$inversions + y2$inversions
    x1 <- y1$sortedVector
    x2 <- y2$sortedVector
    i1 <- 1
    i2 <- 1
    while(i1+i2 <= n1+n2+1){
      if(i2 > n2 || (i1 <= n1 && x1[i1] <= x2[i2])){
        x[i1+i2-1] <- x1[i1]
        i1 <- i1 + 1
      } else {
        inv <- inv + n1 + 1 - i1
        x[i1+i2-1] <- x2[i2]
        i2 <- i2 + 1
      }
    }
  }
  return (list(inversions=inv,sortedVector=x))
}


numberOfInversions <- function(x){
  # Computes number of inversions
  #
  # Args:
  #   x: list with the distance of each item
  #
  # Returns:
  #   Kendall thau, i.e. the number of inversions

  r <- mergeSort(x)
  return (r$inversions)
}

normalizedKendallTauDistance <- function(x,y){
  # Computes normalized kendall tau distance
  #
  # Args:
  #   x: One of two vectors whose distance is to be calculated.
  #   y: The other vector. x and y must have the same length, greater than one,
  #     with no missing values.
  # 
  # Returns:
  #   The normalized Kendall tau distance 
  #
  # Based on http://en.wikipedia.org/wiki/Kendall_tau_distance


  tau = numberOfInversions(order(x)[rank(y)])
  nItens = length(x)
  maxNumberOfInverstions <- (nItens*(nItens-1))/2
  normalized = tau/maxNumberOfInverstions

  return(normalized)
}

args <- commandArgs(trailingOnly = TRUE)

rank1 <- read.table(args[1])
rank2 <- read.table(args[2])
matriz <- merge(rank1, rank2, by="V1")
normalizedKendallTauDistance(matriz$V2.x, matriz$V2.y)
