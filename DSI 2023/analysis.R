


################################ Analysis Script ################################
### this script runs the entire analysis for # Replication code for "The Effect of COVID-19 Infection on Opposition to COVID-19 Policies: Evidence from the U.S. Congress" 


# load packages
library(fect)
library(dplyr)
library(kableExtra)
library(modelsummary)
library(grf)
library(ggplot2) 



# set seed for reproducibility
set.seed(42)


# read in the data
data <- read.csv("analysis_data.csv")



# create function to use the fect package to estimate effects of infection on 
# opposition using matrix completion. All models condition on the total number of tweets. 

estimate <- function(data, formula, seed, estimator) {
  fect(data = data,
       formula = formula,
       method = estimator, ## I used MC in the text, which is more appropriate for the analysis,
       # however fixed effects estimates are very similar and are significantly faster to compute. 
       seed = seed,
       index = c("entity_id", "time_id"),
       r = c(0, 5),
       k = 10,
       min.T0 = 1,
       CV = TRUE,
       force = "two-way",
       se = TRUE,
       parallel = TRUE,
       nboots = 300)
}


################################################
############### Primary Analysis ###############
################################################



# Table 1, column 1: IVHS transformation of DV and no controls
mc_no_controls_IVHS <- estimate(data, 
    asinh(opposition_tweet_count) ~ treatment + total_tweets, 
    seed = 42,
    estimator = "mc")

# Table 1, column 2: Log transformation of DV and no controls
mc_no_controls_log <- estimate(data, 
    log(opposition_tweet_count+.1) ~ treatment + total_tweets,
    seed = 42,
    estimator = "mc")

# Table 1, column 3: No transformation of DV and Covid Cases (state level) as control
mc_with_controls_covid_cases <- estimate(data, 
    opposition_tweet_count ~ treatment + total_tweets + log(covid_cases),
    seed = 42,
    estimator = "mc")

# Table 1, column 4: No transformation of DV and Covid Cases and Deaths (state level) as controls
mc_with_controls_covid_cases_deaths <- estimate(data, 
    opposition_tweet_count ~ treatment + total_tweets + log(covid_cases) + log(covid_deaths),
    seed = 42,
    estimator = "mc")


# Create a table with the results
  ## NOTE: There's no support for FECT objects in the kableExtra package or in common table-making packages in R such as Model Summary, stargazer, or texreg.
## The results must be extracted from the FECT objects and manually formatted into a table.

tab1_col1_results <- round(as.data.frame(mc_no_controls_IVHS$est.avg), 3)
tab1_col2_results <- round(as.data.frame(mc_no_controls_log$est.avg), 3)
tab1_col3_results <- round(as.data.frame(mc_with_controls_covid_cases$est.avg), 3)
tab1_col4_results <- round(as.data.frame(mc_with_controls_covid_cases_deaths$est.avg), 3)

# combine results into a single table 
results <- rbind(tab1_col1_results, tab1_col2_results, tab1_col3_results, tab1_col4_results)

# add the number of observations to the results
results$Observations <- nrow(data)

# transpose the table 
results <- t(results)

# create a LaTeX table
kable(results, 
format = "latex",
booktabs = TRUE,
caption = "Cumulative effects (ATT) of COVID-19 Infection on Opposition to COVID-19 Policies",
digits = 3,
align = "c",
col.names = c("IVHS", "Log", "Covid Cases", "w/ Cases and Deaths")) %>%
kable_styling(latex_options = c("hold_position", "scale_down")) %>%
footnote(general = "Standard errors are presented in parentheses. All results 
presented use matrix completion methods and are estimated using the FECT 
library in R (Liu, Wang, Xu 2022). Models 1 and 2 use an inverse hyperbolic
 sine transformation and log+.1 transformation, respectively. Model 3 
 includes the number of COVID-19 cases per day in each legislator's 
 constituency state. Model 4 includes the number of new cases and new 
 deaths in each legislator's constituency state.") %>%
save_kable("table1.tex") ### Save the table as a .tex file in the output folder


# In the paper, I plot the results in Figure 3 using plotly in Python.
## However, you can print the results using the following code:
#plot(mc_no_controls_IVHS,xlim = c(-1,2))

# save the results into the output folder to plot in Python
estimates = as.data.frame(mc_no_controls_IVHS$est.att)
write.csv(estimates, 'figure3.csv')


# In the paper, I plot the results for the exit effects in Figure 4 using plotly in Python.
## However, you can print the results using the following code:
#plot(mc_no_controls_IVHS,xlim = c(-1,7),type = "exit")


# save the exit effects estimates to plot in python for figure 4 
exit_effects = as.data.frame(mc_no_controls_IVHS$est.att.off)
write.csv(exit_effects, 'figure4.csv')



# save the pre-trends equivalence test results for the Appendix (Figure A2) to the output folder using ggplot2
ggsave(plot(mc_no_controls_IVHS,
type = "equiv",
ylim = c(-4,4),
cex.legend = 0.6,
ylab = "Opposition",
main = "Testing Pre-Trend (FEct)",
cex.text = 0.8,
), filename = "figureA2.png")




################################################################
############# CATE Estimation using Causal Forests #############
################################################################





# move the two senators (sanders king) and who caucus with the Democrats to the Democratic party (per reviewer 3)
data[data$party == 'Independent', 'party'] = 'Democrat'


# convert string variables to numeric for analysis
data$entity_id = as.numeric(as.factor(data$entity_id))
data$Republican = as.numeric(data$party == 'Republican')
data$Male = as.numeric(data$gender == 'M')
data$Age = as.numeric(data$MC_birth_year)
data['Total tweets'] = data['total_tweets']




# create vectors for each variable of interest
Y1_tweets <- data$opposition_tweet_count
W = data$treatment
X = data[c('Republican', 'Male', 'Total tweets', 'Age')]
entity_id_int = as.numeric(as.factor(data$entity_id))


# estimate the CATE using causal forests
cf1 <- causal_forest(X, Y1_tweets, W, W.hat = 0.5, clusters = entity_id_int, num.trees = 5000, seed = 42)


# get the variable importance
varimp_tweets <- variable_importance(cf1)
ranked.vars <- order(varimp_tweets, decreasing = TRUE)


# Top 4 variables according to this measure
colnames(X)[ranked.vars[1:4]]

# estimate the CATE using the top 4 variables
results_tweets = best_linear_projection(cf1, X[ranked.vars[1:4]])


# create a list of the results with the name of the model
models <- list('Opposition Tweets'= results_tweets)



## save the results to a table (Table A2)
modelsummary(models, 
             fmt = 5,
             coef_omit = "Intercept",
             stars = TRUE, 
             digits = 3,
             output = "tableA2.tex")



# View the results using a coefficient plot ( this wasn't in the accepted article)
#modelplot(models, coef_omit = "Intercept",fatten = .7,size = 1) +
# labs(x = 'Coefficient Estimate', y = 'Variable',title = 'CATE estimates Using Causal Forests') + 
# theme(axis.text.x = element_text(angle = 45, hjust = 1)) + 
# theme_minimal() + # add zero line to the plot 
# geom_vline(xintercept = 0, linetype = "dashed", color = "red")






#####################################################
############### Robustness Check 1 ##################
##### Estimation with infected legislators only #####
#####################################################


# This step repeats the first analysis but only includes legislators who were infected with COVID-19.



## get only the entity_ids of infected legislators
infected_ids <- unique(data[data$treatment == 1, 'entity_id'])

#  filter the data to include only infected legislators
infected_df <- data[data$entity_id %in% infected_ids,]





# Table A3, column 1: IVHS transformation of DV and no controls
mc_no_controls_IVHS <- estimate(infected_df, 
    asinh(opposition_tweet_count) ~ treatment + total_tweets,
    seed = 44,
    estimator = "mc")

# Table A3, column 2: Log transformation of DV and no controls
mc_no_controls_log <- estimate(infected_df, 
    log(opposition_tweet_count+.1) ~ treatment + total_tweets,
    seed = 44,
    estimator = "mc")

# Table A3, column 3: 
# No transformation of DV and Covid Cases (state level) as control
mc_with_controls_covid_cases <- estimate(infected_df, 
    opposition_tweet_count ~ treatment + total_tweets + log(covid_cases),
    seed = 44,
    estimator = "mc")

# Table A3, column 4: 
# No transformation of DV and Covid Cases and Deaths (state level) as controls
mc_with_controls_covid_cases_deaths <- estimate(infected_df, 
    opposition_tweet_count ~ treatment + total_tweets + log(covid_cases) + log(covid_deaths),
    seed = 44,
    estimator = "mc")


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
col.names = c("IVHS", "Log", "Covid Cases", "w/ Cases and Deaths")) %>%
kable_styling(latex_options = c("hold_position", "scale_down")) %>%
footnote(general = "Standard errors are presented in parentheses. All results 
presented use matrix completion methods and are estimated using the FECT 
library in R (Liu, Wang, Xu 2022). Models 1 and 2 use an inverse hyperbolic 
sine transformation and log+.1 transformation, respectively. Model 3
 includes the number of COVID-19 cases per day in each legislator's constituency state.
  Model 4 includes the number of new cases and new deaths in each legislator's
   constituency state.") %>%
save_kable("tableA3.tex") ### Save the table as a .tex file in the output folder





#####################################################
############### Robustness Check 2 ##################
##### Estimation with total tweets about COVID ######
#####################################################


# This step repeats the first analysis but estimates the effect of infection on the total number 
# of tweets about COVID-19. The logic of the robustness check is that legislators who were 
# infected with COVID-19 may send fewer tweets in a more general sense when they are infected
# with COVID-19, which may explain the results we observe in the main analysis.






# Table A3, column 1: IVHS transformation of DV and no controls
mc_no_controls_IVHS <- estimate(data, 
    asinh(total_tweets) ~ treatment,
    seed = 44,
    estimator = "mc")

# Table A3, column 2: Log transformation of DV and no controls
mc_no_controls_log <- estimate(data, 
    log(total_tweets+.1) ~ treatment,
    seed = 44,
    estimator = "mc")

# Table A3, column 3: No transformation of DV and Covid Cases (state level) as control
mc_with_controls_covid_cases <- estimate(data, 
    total_tweets ~ treatment + log(covid_cases),
    seed = 44,
    estimator = "mc")

# Table A3, column 4: No transformation of DV and Covid Cases and Deaths (state level) as controls
mc_with_controls_covid_cases_deaths <- estimate(data, 
    total_tweets ~ treatment + log(covid_cases) + log(covid_deaths),
    seed = 44,
    estimator = "mc")


# Create a table with the results
  ## NOTE: There's no support for FECT objects in the kableExtra package or in common table-making packages in R such as Model Summary, stargazer, or texreg.
## The results must be extracted from the FECT objects and manually formatted into a table.

tabA4_col1_results = round(as.data.frame(mc_no_controls_IVHS$est.avg), 3)
tabA4_col2_results = round(as.data.frame(mc_no_controls_log$est.avg), 3)
tabA4_col3_results = round(as.data.frame(mc_with_controls_covid_cases$est.avg), 3)
tabA4_col4_results = round(as.data.frame(mc_with_controls_covid_cases_deaths$est.avg), 3)

# combine results into a single table 
results <- rbind(tabA4_col1_results, tabA4_col2_results, tabA4_col3_results, tabA4_col4_results)

# add the number of observations to the results
results$Observations <- nrow(data)

# transpose the table 
results <- t(results)


# create a LaTeX table
kable(results, 
format = "latex",
booktabs = TRUE,
caption = "Effect of COVID-19 Infection on Total Tweets",
digits = 3,
align = "c",
col.names = c("IVHS", "Log", "Covid Cases", "w/ Cases and Deaths")) %>%
kable_styling(latex_options = c("hold_position", "scale_down")) %>%
footnote(general = "Standard errors are presented in parentheses. All results presented use 
matrix completion methods and are estimated using the FECT library in R (Liu, Wang, Xu 2022).
 Models 1 and 2 use an inverse hyperbolic sine transformation and log+.1 transformation, 
 respectively. Model 3 includes the number of COVID-19 cases per day in each legislator's 
 constituency state. Model 4 includes the number of new cases and new deaths in each 
 legislator's constituency state.") %>%
save_kable("tableA4.tex") ### Save the table as a .tex file in the output folder


#####################################################
############### Robustness Check 3 ##################
##### Estimation with Congress Press Releases #######
#####################################################


# This step repeats the first analysis but estimates the effect of infection 
# on opposition using press releases from the legislator's office as the dependent variable. 







# Table A3, column 1: IVHS transformation of DV and no controls
mc_no_controls_IVHS <- estimate(data, 
    asinh(press_releases_opposition_count) ~ treatment + press_releases_total,
    seed = 44,
    estimator = "mc")

# Table A3, column 2: Log transformation of DV and no controls
mc_no_controls_log <- estimate(data, 
    log(press_releases_opposition_count+.1) ~ treatment + press_releases_total,
    seed = 44,
    estimator = "mc")

# Table A3, column 3: No transformation of DV and Covid Cases (state level) as control
mc_with_controls_covid_cases <- estimate(data, 
    press_releases_opposition_count ~ treatment + press_releases_total + log(covid_cases),
    seed = 44,
    estimator = "mc")

# Table A3, column 4: No transformation of DV and Covid Cases and Deaths (state level) as controls
mc_with_controls_covid_cases_deaths <- estimate(data, 
    press_releases_opposition_count ~ treatment + press_releases_total + log(covid_cases) + log(covid_deaths),
    seed = 44,
    estimator = "mc")


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
col.names = c("IVHS", "Log", "Covid Cases", "w/ Cases and Deaths")) %>%
kable_styling(latex_options = c("hold_position", "scale_down")) %>%
footnote(general = "Standard errors are presented in parentheses. All results 
presented use matrix completion methods and are estimated using the FECT 
library in R (Liu, Wang, Xu 2022). Models 1 and 2 use an inverse hyperbolic 
sine transformation and log+.1 transformation, respectively. Model 3 includes 
the number of COVID-19 cases per day in each legislator's constituency state. 
Model 4 includes the number of new cases and new deaths in each legislator's 
constituency state.") %>%
save_kable("tableA5.tex") ### Save the table as a .tex file in the output folder




# In the paper, I plot the results in Figure A3 using plotly in Python.
## However, you can print the results using the following code:
#plot(mc_no_controls_IVHS,xlim = c(-1,2))

# save the results into the output folder to plot in Python
estimates = as.data.frame(mc_no_controls_IVHS$est.att)
write.csv(estimates, 'figureA3.csv')



#####################################################
############### Robustness Check 4 ##################
#### Estimation using interactive Fixed Effects #####
#####################################################


## Replication of the primary analysis (table A7) using interactive fixed effects 



# estimate interactive fixed effects without controls (Appendix H - table A7, column 1)
ife_no_controls <- estimate(data, 
  opposition_tweet_count ~ treatment + total_tweets,
  seed = 44, 
  estimator = "ife")

# estimate interactive fixed effects with controls (Appendix H - table A7, column 2)
ife_with_controls <- estimate(data, 
  opposition_tweet_count ~ treatment + total_tweets + log(covid_cases) + log(covid_deaths),
  seed = 44,
  estimator = "ife")



# Create a table with the results
  ## NOTE: There's no support for FECT objects in the kableExtra package or in common table-making packages in R such as Model Summary, stargazer, or texreg.
## The results must be extracted from the FECT objects and manually formatted into a table.

tabA7_col1_results <- round(as.data.frame(ife_no_controls$est.avg), 3)
tabA7_col2_results <- round(as.data.frame(ife_with_controls$est.avg), 3)


# combine results into a single table 
results <- rbind(tabA7_col1_results, tabA7_col2_results)

# add the number of observations to the results
results$Observations <- nrow(data)

# transpose the table 
results <- t(results)



# create a LaTeX table
kable(results, 
format = "latex",
booktabs = TRUE,
caption = "Effects of COVID-19 Infection on Opposition to COVID -- Full sample",
digits = 3,
align = "c",
col.names = c("without controls", "with controls")) %>%
kable_styling(latex_options = c("hold_position", "scale_down")) %>%
footnote(general = "Standard errors presented in parentheses. Model 1 uses interactive fixed effects without controls and Model 2 uses interactive fixed effects with controls. Estimations rely on the Fect library in R.") %>%
save_kable("tableA7.tex") ### Save the table as a .tex file in the output folder
# create table




#####################################################
############### Robustness Check 5 ##################
#### Estimation using interactive Fixed Effects #####
#####################################################


# Replication of MC estimation of the effect of COVID-19 infection on 
# opposition using only infected legislators (table A8) using interactive fixed effects



## get only the entity_ids of infected legislators
infected_ids <- unique(data[data$treatment == 1, 'entity_id'])

#  filter the data to include only infected legislators
infected_df <- data[data$entity_id %in% infected_ids,]




# estimate interactive fixed effects without controls (Appendix H - table A8, column 1)
ife_no_controls <- estimate(infected_df, 
   opposition_tweet_count ~ treatment + total_tweets,
   seed = 41, 
   estimator = "ife")

# estimate interactive fixed effects with controls (Appendix H - table A8, column 2)
ife_with_controls <- estimate(infected_df, 
  opposition_tweet_count ~ treatment + total_tweets + log(covid_cases) + log(covid_deaths),
  seed = 41,
  estimator = "ife")



# Create a table with the results
  ## NOTE: There's no support for FECT objects in the kableExtra package or in common table-making packages in R such as Model Summary, stargazer, or texreg.
## The results must be extracted from the FECT objects and manually formatted into a table.

tabA8_col1_results = round(as.data.frame(ife_no_controls$est.avg), 3)
tabA8_col2_results = round(as.data.frame(ife_with_controls$est.avg), 3)


# combine results into a single table 
results <- rbind(tabA8_col1_results, tabA8_col2_results)

# add the number of observations to the results
results$Observations <- nrow(infected_df)

# transpose the table 
results <- t(results)


# create a LaTeX table
kable(results, 
format = "latex",
booktabs = TRUE,
caption = "Effects of Infection on Infected Legislators Only",
digits = 3,
align = "c",
col.names = c("without controls", "with controls")) %>%
kable_styling(latex_options = c("hold_position", "scale_down")) %>%
footnote(general = "Standard errors presented in parentheses. Model 1 uses interactive fixed effects without controls and Model 2 uses interactive fixed effects with controls. Estimations rely on the Fect library in R.") %>%
save_kable("tableA8.tex") ### Save the table as a .tex file in the output folder
# create table








#####################################################
############### Robustness Check 6 ##################
#### Estimation using interactive Fixed Effects #####
#####################################################


# Replication of MC estimation of the effect of COVID-19 infection on the 
# total number of tweets about COVID-19 using interactive fixed effects (Table A9)




# estimate interactive fixed effects without controls (Appendix H - table A9, column 1)
ife_no_controls <- estimate(data, 
   total_tweets ~ treatment,
   seed = 42,
   estimator = "ife")

# estimate interactive fixed effects with controls (Appendix H - table A9, column 2)
ife_with_controls <- estimate(data, 
  total_tweets ~ treatment + log(covid_cases) + log(covid_deaths),
  seed = 42,
  estimator = "ife")



# Create a table with the results
  ## NOTE: There's no support for FECT objects in the kableExtra package or in common table-making packages in R such as Model Summary, stargazer, or texreg.
## The results must be extracted from the FECT objects and manually formatted into a table.

tabA9_col1_results = round(as.data.frame(ife_no_controls$est.avg), 3)
tabA9_col2_results = round(as.data.frame(ife_with_controls$est.avg), 3)


# combine results into a single table 
results <- rbind(tabA9_col1_results, tabA9_col2_results)

# add the number of observations to the results
results$Observations <- nrow(data)

# transpose the table 
results <- t(results)



# create a LaTeX table
kable(results, 
format = "latex",
booktabs = TRUE,
caption = "Effects of Infection on Total Number of Tweets",
digits = 3,
align = "c",
col.names = c("without controls", "with controls")) %>%
kable_styling(latex_options = c("hold_position", "scale_down")) %>%
footnote(general = "Standard errors presented in parentheses. Model 1 uses interactive fixed effects without controls and Model 2 uses interactive fixed effects with controls. Estimations rely on the Fect library in R.") %>%
save_kable("tableA9.tex") ### Save the table as a .tex file in the output folder
# create table








#####################################################
############### Robustness Check 7 ##################
#### Estimation using interactive Fixed Effects #####
#####################################################


# Replication of MC estimation of the effect of COVID-19 infection on 
# opposition using Congressional Press Releases using interactive fixed effects




# estimate interactive fixed effects without controls (Appendix H - table A8, column 1)
ife_no_controls <- estimate(infected_df, 
   press_releases_opposition_count ~ treatment + press_releases_total,
   seed = 41,
   estimator = "ife")

# estimate interactive fixed effects with controls (Appendix H - table A8, column 2)
ife_with_controls <- estimate(infected_df, 
  press_releases_opposition_count ~ treatment + press_releases_total + log(covid_cases) + log(covid_deaths),
  seed = 41,
  estimator = "ife")



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



# create a LaTeX table
kable(results, 
format = "latex",
booktabs = TRUE,
caption = "Effects of Infection on Opposition using Press releases",
digits = 3,
align = "c",
col.names = c("without controls", "with controls")) %>%
kable_styling(latex_options = c("hold_position", "scale_down")) %>%
footnote(general = "Standard errors presented in parentheses. Model 1 uses interactive fixed effects without controls and Model 2 uses interactive fixed effects with controls. Estimations rely on the Fect library in R.") %>%
save_kable("tableA10.tex") ### Save the table as a .tex file in the output folder
# create table



