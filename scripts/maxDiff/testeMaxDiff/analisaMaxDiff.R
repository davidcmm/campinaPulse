#R vetor = as.vector(t(seg[,1:110]))

library(BiasedUrn)
library(AlgDesign)

incomplete.block.design <- function(number.alternatives, number.blocks, alternatives.per.block, n.repeats = 1000){
    # Check that the parameters are appropriate
    # Sawtooth recommends that number.blocks >= 3 * number.alternatives / alternatives.per.block
    if (number.blocks < 3 * number.alternatives / alternatives.per.block)
        warning("It is recomended that number.blocks >= 3 * number.alternatives / alternatives.per.block");
    library(AlgDesign)
    best.result = NULL
    best.D = -Inf
    for (i in 1:n.repeats){
        alg.results <- optBlock(~.,withinData=factor(1:number.alternatives),blocksizes=rep(alternatives.per.block,number.blocks), nRepeats=5000) #BIB
        if (alg.results$D > best.D){
            best.result = alg.results
            best.D = alg.results$D
        }
    }
    design <- matrix(NA,number.blocks,alternatives.per.block, dimnames= list(block = 1:number.blocks, Alternative = 1:alternatives.per.block))
    binary.design <- matrix(0,number.blocks,number.alternatives, dimnames= list(block = 1:number.blocks, alternative = 1:number.alternatives))
    counter <- 0
    for (block in best.result$Blocks){
        counter <- counter + 1
        blck <- unlist(block)
        design[counter,] <- blck
        for (a in blck)
            binary.design[counter,a] <- 1
    }
    n.appearances.per.alternative <- table(as.numeric(design))
    combinations.of.alternatives <- crossprod(table(c(rep(1:number.blocks, rep(alternatives.per.block,number.blocks))), best.result$design[,1]))
    list(binary.design = t(binary.design), design = t(design), frequencies = n.appearances.per.alternative, pairwise.frequencies=combinations.of.alternatives, binary.correlations = round(cor(binary.design),2))
}

setup.flat.data = function(x, number.alternatives){
   n = nrow(x)
   number.sets = ncol(x) / number.alternatives
   data = vector("list",n)
   for (i in 1:n)
   {
       temp.respondent.data = matrix(x[i,],byrow=TRUE,ncol = number.alternatives)
       respondent.data = vector("list",number.sets)
       for (s in 1:number.sets)
          respondent.data[[s]] = as.numeric(temp.respondent.data[s,])
       data[[i]] = respondent.data
		}
compress.data(data)}
 
compress.data = function(x){#Creates a vector for each set where the first entry was best and the last worst
  compress = function(x){
     x.valid = !is.na(x)
     x.position = (1:length(x))[x.valid]
     x.position[order(x[x.valid], decreasing = TRUE)]
  }
  n = length(x)
  number.sets = length(x[[1]])
  number.alternatives = length(x[[1]][[1]])
  data = vector("list",n)
  for (i in 1:n)
   {
       respondent.data = vector("list",number.sets)
       for (s in 1:number.sets)
          respondent.data[[s]] = compress(x[[i]][[s]])
       data[[i]] = respondent.data
		}
class(data) = "maxdiffData"
data}
 
d.marley = function(b,x){
  b.vector = b[x]
  k = length(b.vector)
  ediffs = exp(matrix(b.vector,k,k,byrow=FALSE) - matrix(b.vector,k,k,byrow=TRUE))
ediffs[1,k] / (sum(ediffs) - sum(diag(ediffs)))}
 
d.rlogit = function(b,x){
  eb = exp(b[x])
  k = length(eb)
  d.best = eb[1]/sum(eb)
  d.not.worst = dMWNCHypergeo(c(rep(1,k-2),0), rep(1,k-1),k-2,eb[-1], precision = 1E-7)
d.best * d.not.worst}
 
d.repeated.maxdiff = function(b,x, method){
  prod(as.numeric(lapply(x,b = b,switch(method,marley=d.marley, rlogit = d.rlogit))))}
 
ll.max.diff = function(b,x, maxdiff.method = c("marley","rlogit")[1]){
   b[b > 100] = 100
   b[b < -100] = -100
   sum(log(as.numeric(lapply(x,b = c(0,b),method=maxdiff.method, d.repeated.maxdiff))))
}
 
max.diff.rank.ordered.logit.with.ties = function(stacked.data){
  flat.data = setup.flat.data(stacked.data, ncol(stacked.data))
  solution = optim(seq(.01,.02, length.out = ncol(stacked.data)-1), ll.max.diff,  maxdiff.method  = "rlogit", gr = NULL, x = flat.data, method =  "BFGS", control = list(fnscale  = -1, maxit = 1000, trace = FALSE), hessian = FALSE)
  pars = c(0, solution$par)
  #print (solution)
  names(pars) = dimnames(stacked.data)[[2]]
  list(log.likelihood = solution$value, coef = pars)}
