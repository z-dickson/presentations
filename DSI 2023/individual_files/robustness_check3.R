#####################################################
############### Robustness Check 3 ##################
##### Estimation with Congress Press Releases #######
#####################################################


# This step repeats the first analysis but estimates the effect of infection 
# on opposition using press releases from the legislator's office as the dependent variable. 



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
set.seed(44)


# read in the data
data <- read.csv("analysis_data.csv")




# create function to use the fect package to estimate effects of infection on opposition using matrix completion. All models condition on the total number of tweets. 

estimate <- function(data, formula) {
  fect(data = data,
       formula = formula,
       method = "mc", ## I used MC in the text, which is more appropriate for the analysis,
       # however fixed effects estimates are very similar and are significantly faster to compute. 
       seed = 44,
       index = c("entity_id", "time_id"),
       r = c(0, 10),
       k = 10,
       min.T0 = 1,
       CV = TRUE,
       force = "two-way",
       se = TRUE,
       parallel = TRUE,
       cores = 18, # adjust accordingly 
       nboots = 300)
}


# Table A3, column 1: IVHS transformation of DV and no controls
mc_no_controls_IVHS <- estimate(data, 
    asinh(press_releases_opposition_count) ~ treatment + press_releases_total)

# Table A3, column 2: Log transformation of DV and no controls
mc_no_controls_log <- estimate(data, 
    log(press_releases_opposition_count+.1) ~ treatment + press_releases_total)

# Table A3, column 3: No transformation of DV and Covid Cases (state level) as control
mc_with_controls_covid_cases <- estimate(data, 
    press_releases_opposition_count ~ treatment + press_releases_total + log(covid_cases))

# Table A3, column 4: No transformation of DV and Covid Cases and Deaths (state level) as controls
mc_with_controls_covid_cases_deaths <- estimate(data, 
    press_releases_opposition_count ~ treatment + press_releases_total + log(covid_cases) + log(covid_deaths))


# Create a table with the results
  ## NOTE: There's no support for FECT objects in the kableExtra package or in common table-making packages in R such as Model Summary, stargazer, or texreg.
## The results must be extracted from the FECT objects and manually formatted into a table.

tabA5_col1_results = round(as.data.frame(mc_no_controls_IVHS$est.avg), 4)
tabA5_col2_results = round(as.data.frame(mc_no_controls_log$est.avg), 4)
tabA5_col3_results = round(as.data.frame(mc_with_controls_covid_cases$est.avg), 4)
tabA5_col4_results = round(as.data.frame(mc_with_controls_covid_cases_deaths$est.avg), 4)

# combine results into a single table 
results <- rbind(tabA5_col1_results, tabA5_col2_results, tabA5_col3_results, tabA5_col4_results)

# add the number of observations to the results
results$Observations <- nrow(data)

# transpose the table 
results <- t(results)

results

# create a LaTeX table
kable(results, 
format = "latex",
booktabs = TRUE,
caption = "ATT Estimates -- Opposition Messages in Press Releases",
digits = 3,
align = "c",
col.names = c("IVHS", "Log", "Covid Cases", "w/ Cases and Deaths"), 
caption.placement = "top") %>%
kable_styling(latex_options = c("hold_position", "scale_down")) %>%
footnote(general = "Standard errors are presented in parentheses. All results presented use matrix completion methods and are estimated using the FECT library in R (Liu, Wang, Xu 2022). Models 1 and 2 use an inverse hyperbolic sine transformation and log+.1 transformation, respectively. Model 3 includes the number of COVID-19 cases per day in each legislator's constituency state. Model 4 includes the number of new cases and new deaths in each legislator's constituency state.") %>%
save_kable("tableA5.tex") ### Save the table as a .tex file in the output folder




# In the paper, I plot the results in Figure A3 using plotly in Python.
## However, you can print the results using the following code:
plot(mc_no_controls_IVHS,
xlim = c(-1,2)
)

# save the results into the output folder to plot in Python
estimates = as.data.frame(mc_no_controls_IVHS$est.att)
write.csv(estimates, 'figureA3.csv')
