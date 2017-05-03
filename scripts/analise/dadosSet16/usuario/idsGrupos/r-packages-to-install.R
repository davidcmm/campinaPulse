ipak <- function(pkg){
    new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
    if (length(new.pkg)) 
        install.packages(new.pkg, dependencies = TRUE)
    sapply(pkg, require, character.only = TRUE)
}

# usage
packages <- c("GGally", "dplyr", "ggplot2", "gmodels", "vcd", "lme4", "nlme", "caret", "pscl", "DT", "broom", "readr")
ipak(packages)

#install.packages("GGally", dependencies = TRUE)
#install.packages("dplyr", dependencies = TRUE)
#install.packages("ggplot2", dependencies = TRUE)
#install.packages("gmodels", dependencies = TRUE)
#install.packages("vcd", dependencies = TRUE)
#install.packages("lme4", dependencies = TRUE)
#install.packages("nlme", dependencies = TRUE)
#install.packages("caret", dependencies = TRUE)
#install.packages("pscl", dependencies = TRUE)
#install.packages("DT", dependencies = TRUE)
#install.packages("broom", dependencies = TRUE)
#install.packages("readr", dependencies = TRUE)
#ips: 10.30.0.23 (diego, /local/davidcmm)
