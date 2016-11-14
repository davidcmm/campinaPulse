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

raw_data = read_delim(
  "classifier//classifier_input_wodraw.dat",
  delim = "\t",
  col_types = cols(
    .default = col_double(),
    row = col_integer(),
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

data = raw_data %>% 
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

agrad <- filter(data, !(question %in% c("seguro?", "seguro"))) %>% 
  mutate_at(vars(40:50), scale)
seg <- filter(data, (question %in% c("seguro?", "seguro")))  %>% 
  mutate_at(vars(40:50), scale)

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

create_random_model_w_interact_scaled = function(the_data, optimizer_to_use=""){
  if ( nchar(optimizer_to_use) == 0 ){
    return( glmer( choice ~ scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff) + bair_cat +
            age_cat:(scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) +
            gender:(scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) +
            inc_cat:(scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) + (1|userID), data = the_data, family=binomial() ) )
    
  }else{
    return( glmer( choice ~ scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff) + bair_cat +
            age_cat:(scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) +
            gender:(scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) +
            inc_cat:(scale(d_swidth) + scale(d_mvcars) + scale(d_pcars) + scale(d_trees) + scale(d_mvciclyst) + scale(d_lands) + scale(d_bid) + scale(d_bheig) + scale(d_dbuild) + scale(d_people) + scale(d_graff)) + (1|userID), data = the_data, family=binomial(), control = glmerControl(optimizer=c(optimizer_to_use) ) ) )#optimizers="bobyqa", "Nelder_Mead"
  }
}

seg_random_user <- create_random_model_w_interact(seg, "")
summary(seg_random_user)
cc <- confint(seg_random_user, parm="beta_", level = 0.95, method="boot", nsim=10, parallel="multicore", ncpus=2)#1000
ctab <- cbind(est=fixef(seg_random_user), cc)
rtab <- exp(ctab)
print(">> Safety beta")
print(ctab, digits=3)
print(">> Safety odds ratio")
print(rtab, digits=3)
