

############# CATE Estimation using Causal Forests #############

# List of package names to install
packages_to_install <- c("grf", "dplyr", "kableExtra")

# Check if each package is already installed
for (package_name in packages_to_install) {
  if (!(package_name %in% installed.packages())) {
    # If not installed, install the package
    install.packages(package_name)
  }
}



# load packages
library(dplyr)
library(modelsummary)
library(grf)



# set seed for reproducibility
set.seed(42)


# read in the data
data <- read.csv("analysis_data.csv")


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
cf1 <- causal_forest(X, Y1_tweets, W, W.hat = 0.5, clusters = entity_id_int, num.trees = 5000)


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



# View the results using a coefficient plot ( this wasn't in the accepted article, but it is a good way to visualize the results)
modelplot(models, 
coef_omit = "Intercept",
fatten = .7,
size = 1) + labs(x = 'Coefficient Estimate', y = 'Variable',
title = 'CATE estimates Using Causal Forests') + 
theme(axis.text.x = element_text(angle = 45, hjust = 1)) + 
theme_minimal() + # add zero line to the plot 
geom_vline(xintercept = 0, linetype = "dashed", color = "red")




