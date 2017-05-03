library(stringr)

require(gmodels)
require(vcd)
require(lme4)
library(nlme)
library(caret)
library(pscl)
library(DT)
library(ggplot2)
theme_set(theme_bw())
library(GGally)
library(dplyr, warn.conflicts = F)
library(broom)

library(car)
library(readr)

create_random_model_w_interact = function(the_data, optimizer_to_use=""){
  if ( nchar(optimizer_to_use) == 0 ){
    return( glmer( choice ~ d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff + bair_cat +
            age_cat:(d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff) +
            gender:(d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff) +
            inc_cat:(d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff) + (1|userID), data = the_data, family=binomial() ) )
    
  }else{
    return( glmer( choice ~ d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff + bair_cat +
            age_cat:(d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff) +
            gender:(d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff) +
            inc_cat:(d_swidth + d_mvcars + d_pcars + d_trees + d_mvciclyst + d_lands + d_bid + d_bheig + d_dbuild + d_people + d_graff) + (1|userID), data = the_data, family=binomial(), control = glmerControl(optimizer=c(optimizer_to_use) ) ) )#optimizers="bobyqa", "Nelder_Mead"
  }
}

extract_list_of_urban_features = function(summary_info, all_estimates, all_pvalues){
  estimates <- summary_info$coef[,"Estimate"]
  pvalues <- summary_info$coef[,"Pr(>|z|)"]
  
  for (column in names(estimates)) { 
    all_estimates[[column]] <- append(all_estimates[[column]], estimates[[column]])
    all_pvalues[[column]] <- append(all_pvalues[[column]], pvalues[[column]])
  }
  
  return (list(all_estimates, all_pvalues))
}

#"hom60_mul15/", "hom15_mul60/", "hom40_mul60/", "hom95_mul95/", "jovem15_adulto60/", , "jovem40_adulto60/", "jovem60_adulto15/", "jovem60_adulto40/", "media15_baixa60/", "media40_baixa60/", "media60_baixa15/", "media60_baixa40/" 
for (folder in c("media40_baixa60/")){
  
    g1_files <- list.files(path = folder, pattern = "*_wodraw.dat") #c("runMerged_0_wodraw.dat", "runMerged_1_wodraw.dat")
    if(grepl("jovem", folder)){
        g1 <- "Jovem"
        g2 <- "Adulto"
    }else if(grepl("media", folder)){
        g1 <- "Media"
        g2 <- "Baixa"
    }else{
        g1 <- "Masculino"
        g2 <- "Feminino"
    }
    
    all_estimates_a <- list("(Intercept)"=c(), d_swidth=c(), d_mvcars=c(), d_pcars=c(), d_trees=c(), d_mvciclyst=c(), d_lands=c(), d_bid=c(), d_bheig=c(), d_dbuild=c(), d_people=c(), d_graff=c(), bair_catcatole_centro=c(), bair_catcatole_liberdade=c(), bair_catcentro_catole=c(), bair_catcentro_liberdade=c(), bair_catliberdade_catole=c(), bair_catliberdade_centro=c(), "d_swidth:age_catadulto"=c(), "d_mvcars:age_catadulto"=c(), "d_pcars:age_catadulto"=c(), "d_trees:age_catadulto"=c(), "d_mvciclyst:age_catadulto"=c(), "d_lands:age_catadulto"=c(), "d_bid:age_catadulto"=c(), "d_bheig:age_catadulto"=c(), "d_dbuild:age_catadulto"=c(), "d_people:age_catadulto"=c(), "d_graff:age_catadulto"=c(), "d_swidth:gendermasculino"=c(), "d_mvcars:gendermasculino"=c(), "d_pcars:gendermasculino"=c(), "d_trees:gendermasculino"=c(), "d_mvciclyst:gendermasculino"=c(), "d_lands:gendermasculino"=c(), "d_bid:gendermasculino"=c(), "d_bheig:gendermasculino"=c(), "d_dbuild:gendermasculino"=c(), "d_people:gendermasculino"=c(), "d_graff:gendermasculino"=c(), "d_swidth:inc_catmedia"=c(), "d_mvcars:inc_catmedia"=c(), "d_pcars:inc_catmedia"=c(), "d_trees:inc_catmedia"=c(), "d_mvciclyst:inc_catmedia"=c(), "d_lands:inc_catmedia"=c(), "d_bid:inc_catmedia"=c(), "d_bheig:inc_catmedia"=c(), "d_dbuild:inc_catmedia"=c(), "d_people:inc_catmedia"=c(), "d_graff:inc_catmedia"=c())
all_pvalues_a <- list("(Intercept)"=c(), d_swidth=c(), d_mvcars=c(), d_pcars=c(), d_trees=c(), d_mvciclyst=c(), d_lands=c(), d_bid=c(), d_bheig=c(), d_dbuild=c(), d_people=c(), d_graff=c(), bair_catcatole_centro=c(), bair_catcatole_liberdade=c(), bair_catcentro_catole=c(), bair_catcentro_liberdade=c(), bair_catliberdade_catole=c(), bair_catliberdade_centro=c(), "d_swidth:age_catadulto"=c(), "d_mvcars:age_catadulto"=c(), "d_pcars:age_catadulto"=c(), "d_trees:age_catadulto"=c(), "d_mvciclyst:age_catadulto"=c(), "d_lands:age_catadulto"=c(), "d_bid:age_catadulto"=c(), "d_bheig:age_catadulto"=c(), "d_dbuild:age_catadulto"=c(), "d_people:age_catadulto"=c(), "d_graff:age_catadulto"=c(), "d_swidth:gendermasculino"=c(), "d_mvcars:gendermasculino"=c(), "d_pcars:gendermasculino"=c(), "d_trees:gendermasculino"=c(), "d_mvciclyst:gendermasculino"=c(), "d_lands:gendermasculino"=c(), "d_bid:gendermasculino"=c(), "d_bheig:gendermasculino"=c(), "d_dbuild:gendermasculino"=c(), "d_people:gendermasculino"=c(), "d_graff:gendermasculino"=c(), "d_swidth:inc_catmedia"=c(), "d_mvcars:inc_catmedia"=c(), "d_pcars:inc_catmedia"=c(), "d_trees:inc_catmedia"=c(), "d_mvciclyst:inc_catmedia"=c(), "d_lands:inc_catmedia"=c(), "d_bid:inc_catmedia"=c(), "d_bheig:inc_catmedia"=c(), "d_dbuild:inc_catmedia"=c(), "d_people:inc_catmedia"=c(), "d_graff:inc_catmedia"=c())
all_estimates_s <- list("(Intercept)"=c(), d_swidth=c(), d_mvcars=c(), d_pcars=c(), d_trees=c(), d_mvciclyst=c(), d_lands=c(), d_bid=c(), d_bheig=c(), d_dbuild=c(), d_people=c(), d_graff=c(), bair_catcatole_centro=c(), bair_catcatole_liberdade=c(), bair_catcentro_catole=c(), bair_catcentro_liberdade=c(), bair_catliberdade_catole=c(), bair_catliberdade_centro=c(), "d_swidth:age_catadulto"=c(), "d_mvcars:age_catadulto"=c(), "d_pcars:age_catadulto"=c(), "d_trees:age_catadulto"=c(), "d_mvciclyst:age_catadulto"=c(), "d_lands:age_catadulto"=c(), "d_bid:age_catadulto"=c(), "d_bheig:age_catadulto"=c(), "d_dbuild:age_catadulto"=c(), "d_people:age_catadulto"=c(), "d_graff:age_catadulto"=c(), "d_swidth:gendermasculino"=c(), "d_mvcars:gendermasculino"=c(), "d_pcars:gendermasculino"=c(), "d_trees:gendermasculino"=c(), "d_mvciclyst:gendermasculino"=c(), "d_lands:gendermasculino"=c(), "d_bid:gendermasculino"=c(), "d_bheig:gendermasculino"=c(), "d_dbuild:gendermasculino"=c(), "d_people:gendermasculino"=c(), "d_graff:gendermasculino"=c(), "d_swidth:inc_catmedia"=c(), "d_mvcars:inc_catmedia"=c(), "d_pcars:inc_catmedia"=c(), "d_trees:inc_catmedia"=c(), "d_mvciclyst:inc_catmedia"=c(), "d_lands:inc_catmedia"=c(), "d_bid:inc_catmedia"=c(), "d_bheig:inc_catmedia"=c(), "d_dbuild:inc_catmedia"=c(), "d_people:inc_catmedia"=c(), "d_graff:inc_catmedia"=c())
all_pvalues_s <- list("(Intercept)"=c(), d_swidth=c(), d_mvcars=c(), d_pcars=c(), d_trees=c(), d_mvciclyst=c(), d_lands=c(), d_bid=c(), d_bheig=c(), d_dbuild=c(), d_people=c(), d_graff=c(), bair_catcatole_centro=c(), bair_catcatole_liberdade=c(), bair_catcentro_catole=c(), bair_catcentro_liberdade=c(), bair_catliberdade_catole=c(), bair_catliberdade_centro=c(), "d_swidth:age_catadulto"=c(), "d_mvcars:age_catadulto"=c(), "d_pcars:age_catadulto"=c(), "d_trees:age_catadulto"=c(), "d_mvciclyst:age_catadulto"=c(), "d_lands:age_catadulto"=c(), "d_bid:age_catadulto"=c(), "d_bheig:age_catadulto"=c(), "d_dbuild:age_catadulto"=c(), "d_people:age_catadulto"=c(), "d_graff:age_catadulto"=c(), "d_swidth:gendermasculino"=c(), "d_mvcars:gendermasculino"=c(), "d_pcars:gendermasculino"=c(), "d_trees:gendermasculino"=c(), "d_mvciclyst:gendermasculino"=c(), "d_lands:gendermasculino"=c(), "d_bid:gendermasculino"=c(), "d_bheig:gendermasculino"=c(), "d_dbuild:gendermasculino"=c(), "d_people:gendermasculino"=c(), "d_graff:gendermasculino"=c(), "d_swidth:inc_catmedia"=c(), "d_mvcars:inc_catmedia"=c(), "d_pcars:inc_catmedia"=c(), "d_trees:inc_catmedia"=c(), "d_mvciclyst:inc_catmedia"=c(), "d_lands:inc_catmedia"=c(), "d_bid:inc_catmedia"=c(), "d_bheig:inc_catmedia"=c(), "d_dbuild:inc_catmedia"=c(), "d_people:inc_catmedia"=c(), "d_graff:inc_catmedia"=c())
    
    for ( i in seq(1, length(g1_files)) ){
        current_file <- paste(folder, g1_files[i], sep="")

        pairwise = read_delim(
          current_file,
          delim = "\t",
          col_types = cols(
            .default = col_double(),
            choice = col_character(),
            question = col_character(),
            photo1 = col_character(),
            photo2 = col_character(),
            choice = col_integer(),
            userID = col_integer(),
            gender = col_character(),
            age = col_character(),
            income = col_character(),
            education = col_character(),
            city = col_character(),
            marital = col_character(),
            graffiti1 = col_character(),
            bairro1 = col_character(),
            graffiti2 = col_character(),
            bairro2 = col_character()
            )
          )
        
        data = pairwise %>% 
          mutate( # Recode
            income = if_else(is.na(income), "media", income),
            age_cat = if_else(as.integer(age) >= 25 | is.na(age), "adulto", "jovem"),
            inc_cat = if_else(income %in% c("baixa", "media baixa"),
                                 "baixa", 
                                 "media"), # substituirá os NA
            choice = if_else(choice == "1", "0", 
                               if_else(choice == "-1", "1", choice)), 
            bair_cat = if_else(bairro1 == bairro2, "mesmo", 
                               paste0(bairro1, "_", bairro2))    
            ) %>% 
          mutate_at( # to factor
            vars(income, age_cat, inc_cat, choice, bair_cat, marital, gender),
            as.factor) %>% 
          mutate( # relevel
            bair_cat = relevel(bair_cat,  "mesmo"),
            marital = relevel(marital,  "solteiro"),
            income = relevel(income,  "baixa"),
            age_cat = relevel(age_cat,  "jovem"),
            gender = relevel(gender,  "feminino"),
            inc_cat = relevel(inc_cat,  "baixa")
          ) 
        
        # Create diff features
        data = data %>%
          mutate(
            d_swidth = street_wid1 - street_wid2,
            d_mvcars = mov_cars1 - mov_cars2,
            d_pcars = park_cars1 - park_cars2,
            d_trees = trees1 - trees2,
            d_mvciclyst = mov_ciclyst1 - mov_ciclyst2,
            d_lands = landscape1 - landscape2,
            d_bid = build_ident1 - build_ident2,
            d_bheig = log2(build_height1 + 1) - log2(build_height2 + 1),
            d_dbuild = diff_build1 - diff_build2,
            d_people = people1 - people2,
            d_graff = (graffiti1 == "Yes") - (graffiti2 == "Yes")
          )
        
        
        agrad_nscaled <- filter(data, !(question %in% c("seguro?", "seguro")))
        seg_nscaled <- filter(data, (question %in% c("seguro?", "seguro")))
        
        agrad_random_user_nscaled <- create_random_model_w_interact(agrad_nscaled, "")
        sum_agrad <- summary(agrad_random_user_nscaled)
        partial_data <- extract_list_of_urban_features(sum_agrad, all_estimates_a, all_pvalues_a)
        all_estimates_a <- partial_data[[1]]
        all_pvalues_a <- partial_data[[2]]
        
        seg_random_user <- create_random_model_w_interact(seg_nscaled, "")
        sum_seg <- summary(seg_random_user)
        partial_data <- extract_list_of_urban_features(sum_seg, all_estimates_s, all_pvalues_s)
        all_estimates_s <- partial_data[[1]]
        all_pvalues_s <- partial_data[[2]]
    }

    print(paste(">>>>> Groups ", g1, g2, folder))
    for (column in names(all_estimates_a)) { 
        print( paste("#### Agrad Values", column, mean(all_estimates_a[[column]])) )
        print( paste("#### Agrad PValues", column, mean(all_pvalues_a[[column]])) )
        print( paste("#### Agrad PValues", column, sum(all_pvalues_a[[column]] < 0.05)) )
    } 
    
    for (column in names(all_estimates_s)) { 
        print( paste("#### Seg Values", column, mean(all_estimates_s[[column]])) )
        print( paste("#### Seg PValues", column, mean(all_pvalues_s[[column]])) )
        print( paste("#### Seg PValues", column, sum(all_pvalues_s[[column]] < 0.05)) )
    }  
}
