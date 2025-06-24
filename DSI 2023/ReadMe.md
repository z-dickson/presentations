# Replication for: *The Effects of COVID-19 Infection on Opposition to COVID-19 Policies: Evidence from the U.S. Congress*



**Authors:** Zach Dickson (LSE) and T. Murat Yildirim (Stavanger)

**Journal:** *Political Communication* 



To run the entire analysis, you will need to have [R](https://www.r-project.org/) and [Python](https://www.python.org/downloads/) installed on your machine. 

There are eight files necessary for replication that are in the main directory:

1. `master.py` - This file runs the entire analysis.
2. `analysis.R` - This file runs all R code 
3. `figures.py` - This file runs all Python code
4. `analysis_data.csv` - The primary dataset used in the analysis (a variable list is provided at the bottom)
5. `covid_infections.csv` - The data file for COVID infections in legislators
6. `validation_tweets.csv` - The data file for the held-out tweets used to validate the language model
7. `py_requirements.txt` - Python library requirements 
8. `requirements.R` - R library requirements 

Additionally, there are two folders that contain the individuals scripts for the analysis (`individual_files`) and all the compiled files (`compiled_files`). If these are not of interest, you can delete both folders and just compile the entire replication using the `master.py` file. Clone the repo, navigate to the new directory and run the following in your terminal: 

```python3 master.py```

**Time to Run:** All scripts executed in 1545.90 seconds (~26 minutes) on 20 core, 64GB RAM machine. It will probably take closer to an hour on a laptop, depending on the number of CPU cores. 

**Notes:**

- The master file calls the two analysis files in R and Python. The R file estimates the primary models, and the Python file creates the figures and tables. These files will save the results in the main directory. 
- There are also two requirements files for each language (`requirements.R` and `py_requirements.txt`) 
- There are two additional folders in the repo that contain the following: 
    - `individual_files` contains the individual analysis files which are broken up by each type of analysis (i.e. one for each table in the article) 
    - `compiled_files` contains all the compiled files for the paper. These file were compiled previously by the author.
- I tried to set seeds where possible to ensure reproducibility, but many of the models are stochastic and may not be exactly the same as in the paper. 




## Files in the `individual_files` folder: 

- `analysis_MC.R` contains the code to reproduce the primary analysis in the paper using Matrix Completion methods. 
- `figures.ipynb` contains the code to reproduce many of the figures and the descriptive statistics presented in the paper (Python notebook).
- `causal_forest.R` contains the code to reproduce estimation of heterogeneous treatment effects using the causal forest method.
- `robustness_check1.R` contains the code to reproduce the robustness check using matrix completion with infected legislators only.
- `robustness_check2.R` contains the code to reproduce the estimation of infection on the number of total tweets from legislators using matrix completion.
- `robustness_check3.R` contains the code to reproduce the estimation of effects of infection on opposition using Congressional Press releases using matrix completion.
- `robustness_check4.R` contains the code to reproduce the estimation of effects of infection on opposition using interactive fixed effects estimator.
- `robustness_check5.R` contains the code to reproduce the estimation of effects of infection on opposition using interactive fixed effects estimator with infected legislators only.
- `robustness_check6.R` contains the code to reproduce the estimation of effects of infection on total tweets using interactive fixed effects estimator.
- `robustness_check7.R` contains the code to reproduce the estimation of effects of infection on total tweets using interactive fixed effects estimator with Congressional Press Releases.


## Files in the `compiled_files` folder:

### Article Manuscript 
- `article.pdf` is the accepted version of the manusript


### Tables 

- `table1.tex` contains the table 1 in the paper (cumulative effects of COVID infection on opposition)
- `tableA1.tex` contains the table A1 in the Appendix (descriptive statistics for tweets)
- `tableA2.tex` contains the table A2 in the Appendix (CATE estimates using causal forest)
- `tableA3.tex` contains the table A3 in the Appendix (Estimation with infected legislators only - Robustness check)
- `tableA4.tex` contains the table A4 in the Appendix (Estimation of infections on the number of total tweets from legislators)
- `tableA5.tex` contains the table A5 in the Appendix (Estimation of effects of infection on opposition using Congressional Press releases)
- `tableA6.tex` contains the table A6 in the Appendix (Descriptive statistics for Congressional Press Releases)
- `tableA7.tex` contains the table A7 in the Appendix (Estimation of effects of infection on opposition using interactive fixed effects estimator)
- `tableA8.tex` contains the table A8 in the Appendix (Estimation of effects of infection on opposition using interactive fixed effects estimator with infected legislators only)
- `tableA9.tex` contains the table A9 in the Appendix (Estimation of effects of infection on total tweets using interactive fixed effects estimator)
- `tableA10.tex` contains the table A10 in the Appendix (Estimation of effects of infection on total tweets using interactive fixed effects estimator with Congressional Press Releases)


### Figures

- `figure1.png` contains the figure 1 in the paper (COVID infections in legislators)
- `figure2.png` contains the figure 2 in the paper (opposition to COVID measures by legislators)
- `figure3.png` contains the figure 3 in the paper (effects of COVID infection on opposition 4 weeks before and after the infection)
- `figure4.png` contains the figure 4 in the paper (exit effects of COVID infection on opposition)
- `figureA1.png` contains the figure A1 in the Appendix (F1 scores for validation of language model)
- `figureA2.png` contains the figure A2 in the Appendix (Pre-trends equivalence tests for matrix completion method)
- `figureA3.png` contains the figure A3 in the Appendix (effects of COVID infection on opposition 4 weeks before and after the infection using Congressional Press Releases - Robustness check)




## Data 
All data (that are not results output of models) are in .csv format and are in the main repo. The data includes the following files:

- `analysis_data.csv` contains the primary dataset used in the analysis
- `covid_infections.csv` contains the data file used to create figure 1 in the paper (COVID infections in legislators)
- `validation_tweets.csv` contains the 1000 held-out tweets used to validate the language model with the model's predictions. 




## Additional Notes: 

The fine-tuned BERT model used in the analysis is available at [this link](https://huggingface.co/z-dickson/US_politicians_covid_skepticism). The model can be loaded using the following code in Python: 

```python
# Load the necessary libraries
from transformers import BertTokenizer, BertForSequenceClassification, pipeline

# Load the model and tokenizer
model_name = 'z-dickson/US_politicians_covid_skepticism'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Load the model into a pipeline
classifier = pipeline('sentiment-analysis',
                       model=model,
                       tokenizer=tokenizer)

# Example usage
classifier("I am skeptical about COVID-19 measures")
```


## Descriptions of the Data Sources 

There are several sources of data that were used, which are detailed below: 

1. The primary data source for legislators' tweets was the Twitter API. This has since been discontinued; however, the data can be collected using the `congresstweets` repo in github ([https://github.com/alexlitel/congresstweets](https://github.com/alexlitel/congresstweets)). 

2. The secondary source of data for the outcome variable using Legislators' press releases came from the ProPublica Congress API ([https://projects.propublica.org/api-docs/congress-api/statements/](https://projects.propublica.org/api-docs/congress-api/statements/)). An account is required to access the API. 

3. The data on COVID-19 infections in legislators was collected from GovTrack ([https://www.govtrack.us/covid-19](https://www.govtrack.us/covid-19)). You can download that data from the website directly. Additionally, I provide the code in the `figures.ipynb` file to import the data directly from the website.

4. The data on COVID-19 infections in the general population (at the state level) was collected from the New York Times COVID-19 data repository ([https://github.com/nytimes/covid-19-data](https://github.com/nytimes/covid-19-data)). You can download the data from the website directly.



# Variable list: 


The primary analysis file (`analysis_data.csv`) is indexed by legislator and time. Additionally, the dataset contains several variables: 


- `entity_id` - an ID variable for each legislator
- `time_id` - a time ID variable (an int for each two-week period)
- `opposition_tweet_count` - the number of tweets that expressed opposition to COVID policies
- `total_tweets` - the number of total tweets about COVID
- `treatment` - a treatment indicator that takes the value of 1 upon infection and for four weeks (two time periods) following. The variable is 0 in all other cases 
- `party` - political party of legislator
- `gender` - gender of legislator 
- `MC_birth_year` - birth year of legislator 
- `press_releases_opposition_count` - the number of press releases that expressed opposition to COVID policies 
- `press_releases_total` - the number of total press releases about COVID
- `date` - date 
- `state` - state of legislator's constituency 
- `covid_cases` - number of cummulative COVID cases for the corresponding state/date (over the two week period) 
- `covid_deaths` - number of cumulative COVID deaths for the corresponding state/date (over the two week period)





# Troubleshooting 

Most folks probably already have R, but Python is probably less common and can be a pain to install. I've always used [anaconda](https://docs.anaconda.com/free/anaconda/install/index.html) (or [Miniconda](https://docs.anaconda.com/free/miniconda/)) to manage python environments. 

Pip should install with python, but you'll get a pip error when running the `py_requirements.txt` file if you don't already have pip installed. There are several potential solutions: 

- install pip [https://packaging.python.org/en/latest/tutorials/installing-packages/](https://packaging.python.org/en/latest/tutorials/installing-packages/)
- Run the notebook in [Google Colab](https://colab.research.google.com/)
    - Google Colab offers a subscription service (and a free version I think) that allows you to run Jupyter notebooks online. It also provides support for R and it allows you to link your Google Drive account to the notebook, which can be super handy to save/import files and code.    


If you still can't run the `master.py` file, you can just run the R file and print the results in R to confirm the replication. The `figures.py` file just makes the figures with results from the models run in R. The [`Fect`](https://yiqingxu.org/packages/fect/articles/tutorial.html) library also will plot the results of the matrix completion and interactive fixed effects models. These plots appear slightly different but they present the same data.  

If you run into any additional problems or issues, feel free to get in contact by raising an issue on Github or via email at zachdickson94@gmail.com.  

