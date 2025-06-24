#####################################################
############### Robustness Check 7 ##################
#### Estimation using interactive Fixed Effects #####
#####################################################


# Replication of MC estimation of the effect of COVID-19 infection on 
# opposition using Congressional Press Releases using interactive fixed effects



# List of package names to install
packages_to_install <- c("fect", "dplyr", "kableExtra")

# Check if each package is already installed
for (package_name in packages_to_install) {
  if (!(package_name %in% installed.packages())) {
    # If not installed, install the package
    install.packages(package_name)
  }
}


# load packages
library(fect)
library(dplyr)
library(kableExtra)


# set seed for reproducibility
set.seed(41)

# read in the data
data <- read.csv("analysis_data.csv")





# create function to use the fect package to estimate interactive fixed effects
estimate <- function(data, formula) {
  fect(data = data,
       formula = formula,
       method = "ife",  ## change method to "ife" to estimate interactive fixed effects
       seed = 41,
       index = c("entity_id", "time_id"),
       r = c(0, 5),
       CV = TRUE,
       force = "two-way",
       se = TRUE,
       parallel = TRUE,
       cores = 16,
       nboots = 300)
}




# estimate interactive fixed effects without controls (Appendix H - table A8, column 1)
ife_no_controls <- estimate(infected_df, 
   press_releases_opposition_count ~ treatment + press_releases_total)

# estimate interactive fixed effects with controls (Appendix H - table A8, column 2)
ife_with_controls <- estimate(infected_df, 
  press_releases_opposition_count ~ treatment + press_releases_total + log(covid_cases) + log(covid_deaths))



# Create a table with the results
  ## NOTE: There's no support for FECT objects in the kableExtra package or in common table-making packages in R such as Model Summary, stargazer, or texreg.
## The results must be extracted from the FECT objects and manually formatted into a table.

tabA10_col1_results = round(as.data.frame(ife_no_controls$est.avg), 3)
tabA10_col2_results = round(as.data.frame(ife_with_controls$est.avg), 3)


# combine results into a single table 
results <- rbind(tabA10_col1_results, tabA10_col2_results)

# add the number of observations to the results
results$Observations <- nrow(data)

# transpose the table 
results <- t(results)

results

# create a LaTeX table
kable(results, 
format = "latex",
booktabs = TRUE,
caption = "Effects of Infection on Opposition using Press releases",
digits = 3,
align = "c",
col.names = c("without controls", "with controls"), 
caption.placement = "top") %>%
kable_styling(latex_options = c("hold_position", "scale_down")) %>%
footnote(general = "Standard errors presented in parentheses. Model 1 uses interactive fixed effects without controls and Model 2 uses interactive fixed effects with controls. Estimations rely on the Fect library in R.") %>%
save_kable("tableA10.tex") ### Save the table as a .tex file in the output folder
# create table


