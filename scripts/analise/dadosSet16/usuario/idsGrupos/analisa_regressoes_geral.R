extract_list_of_urban_features_general = function(summary_info, all_estimates, all_pvalues){
  estimates <- summary_info$coef[,"Estimate"]
  pvalues <- summary_info$coef[,"Pr(>|t|)"]
  
  for (column in names(estimates)) { 
    all_estimates[[column]] <- append(all_estimates[[column]], estimates[[column]])
    all_pvalues[[column]] <- append(all_pvalues[[column]], pvalues[[column]])
  }
  
  return (list(all_estimates, all_pvalues))
}

#Combining all street features
combineFeaturesAndTestRegression <- function(dataset){
    
      colnames(dataset)[colnames(dataset) == "V2"] <- "image_url"
      temp <- merge(groupedData1, dataset, by.x="image_url", by.y="image_url")
      temp <- merge(temp, groupedData2, by.x="image_url", by.y="image_url")
      temp <- merge(temp, groupedData3, by.x="image_url", by.y="image_url")
      temp <- merge(temp, groupedData4, by.x="image_url", by.y="image_url")
      temp <- merge(temp, groupedData5, by.x="image_url", by.y="image_url")
      temp <- merge(temp, groupedData6, by.x="image_url", by.y="image_url")
      temp <- merge(temp, groupedData7, by.x="image_url", by.y="image_url")
      temp <- merge(temp, groupedData8, by.x="image_url", by.y="image_url")
      temp<- merge(temp, groupedData9, by.x="image_url", by.y="image_url")
      temp <- merge(temp, groupedData10, by.x="image_url", by.y="image_url")
      temp <- merge(temp, groupedData11, by.x="image_url", by.y="image_url")
      temp <- merge(temp, groupedData12, by.x="image_url", by.y="image_url")
      temp <- merge(temp, groupedData13, by.x="image_url", by.y="image_url")
      
      temp1 <- lapply(as.character(temp$image_url), function (x) strsplit(x, split="/", fixed=TRUE)[[1]][6])
      neigs1 <- unlist(lapply(temp1, '[[', 1))
      temp$bairro <- neigs1
      
      temp <- arrange(temp, mean)  %>% mutate(rank = 1:n())
      temp$centro <- 0
      temp$catole <- 0
      temp$liberdade <- 0
      temp$centro[temp$bairro == "centro"] <- 1
      temp$catole[temp$bairro == "catole"] <- 1
      temp$liberdade[temp$bairro == "liberdade"] <- 1
      temp$graffiti <- factor(temp$graffiti, levels = c("Yes", "No"))
      temp$graffiti <- relevel(temp$graffiti,  "No")
      
      regGeneral <- lm(rank ~  street_wid + mov_cars + park_cars + mov_ciclyst + landscape + build_ident + trees + log2(build_height+1) + people + centro + catole + liberdade + diff_build + graffiti, na.action = na.exclude, data = temp)
      print(summary(regGeneral))
      return(summary(regGeneral))
}

for (folder in c("hom15_mul60/", "hom40_mul60/", "hom95_mul95/", "hom60_mul15/", "jovem15_adulto60/", "jovem40_adulto60/", "jovem60_adulto15/", "jovem60_adulto40/", "jovem80_adulto80/", "media15_baixa60/", "media40_baixa60/", "media60_baixa15/", "media60_baixa40/", "jovem60_adulto60/", "hom60_mul60/", "media60_baixa60/")){

  if(grepl("jovem", folder)){
        g1 <- "Jovem"
        g2 <- "Adulto"
  }else if(grepl("media", folder)){
        g1 <- "Media"
        g2 <- "Baixa"
  }else{
        g1 <- "masculino" #"Masculino"
        g2 <- "feminino" #"Feminino"
  }
  
  all_diff_m <- list.files(path = folder, pattern = "allDiff*_*")
  
  all_original <- read.table("../all100/all_ordenado.dat")
  ag_orig <- filter(all_original, V1 != "seguro?")
  seg_orig <- filter(all_original, V1 == "seguro?")
  
  all_means_ag_g1 <- data.frame()
  all_means_seg_g1 <- data.frame()
  
  all_estimates_a <- list("(Intercept)"=c(), street_wid=c(), mov_cars=c(), park_cars=c(), trees=c(), mov_ciclyst=c(), landscape=c(), build_ident=c(), "log2(build_height + 1)"=c(), diff_build=c(), people=c(), d_graff=c(), centro=c(), catole=c(), liberdade=c(), graffitiYes=c())
all_pvalues_a <- list("(Intercept)"=c(), street_wid=c(), mov_cars=c(), park_cars=c(), trees=c(), mov_ciclyst=c(), landscape=c(), build_ident=c(), "log2(build_height + 1)"=c(), diff_build=c(), people=c(), d_graff=c(), centro=c(), catole=c(), liberdade=c(), graffitiYes=c())

  all_estimates_s <- list("(Intercept)"=c(), street_wid=c(), mov_cars=c(), park_cars=c(), trees=c(), mov_ciclyst=c(), landscape=c(), build_ident=c(), "log2(build_height + 1)"=c(), diff_build=c(), people=c(), d_graff=c(), centro=c(), catole=c(), liberdade=c(), graffitiYes=c())
  all_pvalues_s <- list("(Intercept)"=c(), street_wid=c(), mov_cars=c(), park_cars=c(), trees=c(), mov_ciclyst=c(), landscape=c(), build_ident=c(), "log2(build_height + 1)"=c(), diff_build=c(), people=c(), d_graff=c(), centro=c(), catole=c(), liberdade=c(), graffitiYes=c())
  
  for (i in seq(1,100)){
     print(paste("########### Iteration ", i))
     
     #General ranking removing men
     current_file <- paste(folder, all_diff_m[i], sep="")
     data <- read.table(current_file)
     seg_g1 <- filter(data, V1 == "seguro?") %>% do(arrange(., V3)) %>%
mutate(rank = 1:n())
     ag_g1 <- filter(data, V1 != "seguro?") %>% do(arrange(., V3)) %>%
mutate(rank = 1:n())
     
      #Extracting features for current regression and saving them!
      sum_agrad <- combineFeaturesAndTestRegression(all_means_ag_g1)
      sum_seg <- combineFeaturesAndTestRegression(all_means_seg_g1)
      
      partial_data <- extract_list_of_urban_features_general(sum_agrad, all_estimates_a, all_pvalues_a)
      all_estimates_a <- partial_data[[1]]
      all_pvalues_a <- partial_data[[2]]
      partial_data <- extract_list_of_urban_features_general(sum_seg, all_estimates_s, all_pvalues_s)
      all_estimates_s <- partial_data[[1]]
      all_pvalues_s <- partial_data[[2]]
  }

    sink(paste(folder, "regressions.dat", sep=""), append=TRUE)
    print(paste(">>>>> Groups ", g1, g2, folder))
    for (column in names(all_estimates_a)) { 
        print( paste("#### Agrad Values", column, mean(all_estimates_a[[column]])) )
        print( paste("#### Agrad PValues", column, mean(all_pvalues_a[[column]])) )
        print( paste("#### Agrad PValues", column, sum(all_pvalues_a[[column]] < 0.05)) / length(all_pvalues_a[[column]]) )
    } 
    
    for (column in names(all_estimates_s)) { 
        print( paste("#### Seg Values", column, mean(all_estimates_s[[column]])) )
        print( paste("#### Seg PValues", column, mean(all_pvalues_s[[column]])) )
        print( paste("#### Seg PValues", column, sum(all_pvalues_s[[column]] < 0.05)) / length(all_pvalues_a[[column]]) )
    }
    sink()
}
