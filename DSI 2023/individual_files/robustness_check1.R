
#####################################################
############### Robustness Check 1 ##################
##### Estimation with infected legislators only #####
#####################################################


# This step repeats the first analysis but only includes legislators who were infected with COVID-19.



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



## get only the entity_id of infected legislators
infected_ids <- unique(data[data$treatment == 1, 'entity_id'])

#  filter the data to include only infected legislators
infected_df <- data[data$entity_id %in% infected_ids,]



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
mc_no_controls_IVHS <- estimate(infected_df, 
    asinh(opposition_tweet_count) ~ treatment + total_tweets)

# Table A3, column 2: Log transformation of DV and no controls
mc_no_controls_log <- estimate(infected_df, 
    log(opposition_tweet_count+.1) ~ treatment + total_tweets)

# Table A3, column 3: No transformation of DV and Covid Cases (state level) as control
mc_with_controls_covid_cases <- estimate(infected_df, 
    opposition_tweet_count ~ treatment + total_tweets + log(covid_cases))

# Table A3, column 4: No transformation of DV and Covid Cases and Deaths (state level) as controls
mc_with_controls_covid_cases_deaths <- estimate(infected_df, 
    opposition_tweet_count ~ treatment + total_tweets + log(covid_cases) + log(covid_deaths))


# Create a table with the results
  ## NOTE: There's no support for FECT objects in the kableExtra package or in common table-making packages in R such as Model Summary, stargazer, or texreg.
## The results must be extracted from the FECT objects and manually formatted into a table.

tabA3_col1_results = round(as.data.frame(mc_no_controls_IVHS$est.avg), 3)
tabA3_col2_results = round(as.data.frame(mc_no_controls_log$est.avg), 3)
tabA3_col3_results = round(as.data.frame(mc_with_controls_covid_cases$est.avg), 3)
tabA3_col4_results = round(as.data.frame(mc_with_controls_covid_cases_deaths$est.avg), 3)

# combine results into a single table 
results <- rbind(tabA3_col1_results, tabA3_col2_results, tabA3_col3_results, tabA3_col4_results)

# add the number of observations to the results
results$Observations <- nrow(infected_df)

# transpose the table 
results <- t(results)


# create a LaTeX table
kable(results, 
format = "latex",
booktabs = TRUE,
caption = "Estimation with Infected Legislators Only",
digits = 3,
align = "c",
col.names = c("IVHS", "Log", "Covid Cases", "w/ Cases and Deaths"), 
caption.placement = "top") %>%
kable_styling(latex_options = c("hold_position", "scale_down")) %>%
footnote(general = "Standard errors are presented in parentheses. All results presented use matrix completion methods and are estimated using the FECT library in R (Liu, Wang, Xu 2022). Models 1 and 2 use an inverse hyperbolic sine transformation and log+.1 transformation, respectively. Model 3 includes the number of COVID-19 cases per day in each legislator's constituency state. Model 4 includes the number of new cases and new deaths in each legislator's constituency state.") %>%
save_kable("tableA3.tex") ### Save the table as a .tex file in the output folder
