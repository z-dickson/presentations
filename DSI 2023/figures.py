


# import required packages
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# create a config class to store colors and font for all figures 
class config: 
    colors = [ '#387da8', '#cf514e']
    font = 'Arial'
    dem = 'rgb(0, 174, 243)'
    rep = 'rgb(232, 27, 35)'
    
    
# Figure 1: COVID-19 Infections Among US Legislators

### You can pull this data from the web using the code below. 

### Alternatively, I have also saved a copy of the final data required just to make the figure, so you can skip the next cell and directly use the data from the cell after that.


"""## get dates of infection for US legislators from govtrack data:  https://www.govtrack.us/covid-19
covid = pd.read_html('https://www.govtrack.us/covid-19')[0]

# create a date column
covid['date'] = pd.to_datetime(covid.Date)

# replace the names that include the title and district in parentheses with just the name
covid['name'] = covid.Legislator.str.replace('Rep.', '').str.replace('Sen.', '').str.strip().str.split("(").str.get(0).str.strip()

# end date of infections at 2022-05-01
covid = covid.loc[covid.date <= '2022-05-01']

# create a new infections column with 1 for each infection
covid['new_infections'] = 1

# group by week and aggregate new infections and cumulative infections
c = covid.groupby(pd.Grouper(key='date', freq='W')).agg({'new_infections': 'sum'}).reset_index()

# create a cumulative infections column
c['cumulative_infections'] = c.new_infections.cumsum()

# create a text column for the new infections and cumulative infections
c['new_infections_text'] = c['new_infections'].replace(0, np.nan)

# create a text column for the new infections and cumulative infections (for the figure)
c.loc[c.cumulative_infections==258, 'cumulative_infections_text'] = 258
c.loc[c.cumulative_infections==136, 'cumulative_infections_text'] = 136"""

################### Make figure 1 #####################


# read data from csv
c = pd.read_csv('covid_infections.csv')


# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])


colors = px.colors.qualitative.T10

fig.add_trace(go.Scatter(x=c.date, y=c['new_infections'], name='New Infections', mode='lines', marker_size=6, marker_symbol='diamond', 
                         marker_line_width=.1, marker_color=colors[1], marker_line_color='black',text=c.new_infections_text, 
                         textposition="top right", textfont=dict(size=16, family=config.font), line=dict(width=1)), secondary_y=False)

fig.add_trace(go.Scatter(x=c.date, y=c['cumulative_infections'], name='Cumulative Infections', mode='lines', marker_size=6, marker_symbol='diamond',
                            marker_line_width=.1, marker_color=colors[0], marker_line_color='black', text=c.cumulative_infections_text,
                            textposition="top center", textfont=dict(size=14, family=config.font), line=dict(width=1)), secondary_y=True)


fig.update_layout(
    font_family="Arial",
    font_color="black",
    title_font_family="Arial",
    title_font_color="black",
    title_font_size = 22,
    font_size = 16,
    legend_title_font_color="black", 
    template='presentation',
    yaxis_title="New Infections",
    yaxis2_title="Cumulative Infections",
    xaxis_tickformat='%b %Y',
    xaxis_title="",
    title_x=0.05, 
    width=800,
    height=500,
    showlegend=True,
    )

## move legend to horizontal
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=.55,
    font_size=18,
    ), legend_title_text='')

## add annotation in bottom right corner
fig.add_annotation(
    x=1.0,
    y=-.16,
    text="<b>Data Source:</b> GovTrack",
    showarrow=False,
    xref="paper",
    yref="paper",
    font=dict(size=16, color="black", family=config.font),
)


# reduce margins 
fig.update_layout(margin=dict(l=70, r=40, t=50, b=90, pad=1))

# make lines thicker
fig.update_traces(line=dict(width=4))

#fig.show()
fig.write_image('figure1.png', scale=2)


# Figure 2: Opposition to COVID-19 Policies by Political Party

# read dataset 
df = pd.read_csv('analysis_data.csv')

# convert date to datetime
df.date = pd.to_datetime(df.date)

# make the two independent senators democrats since they caucus with the democrats
df.party = df.party.replace({'Independent': 'Democrat'})

# create an opposition percentage column 
df['opposition'] = df['opposition_tweet_count'] / df.total_tweets

# group the dataset by party and date and calculate the mean and standard error of the opposition
party = df.groupby(['party', 'date']).agg({'opposition': ['mean', 'sem']}).reset_index()

# rename columns
party.columns = ['party', 'date', 'opposition', 'sem']

    
# create the plot
fig = px.line(party, x='date', y='opposition', color='party', color_discrete_sequence=[config.dem, config.rep],
              labels={'date':'Date', 'opposition':'Opposition'}, 
              title='Opposition to COVID-19 Policies by Party', 
              )


for p in party.party.unique():
    x1 = party.loc[party.party == p]
    if p == 'Democrat':
        color = 'rgba(0,176,246,0.2)'
    if p == 'Republican':
        color = 'rgba(255,0,0,0.2)'
    
    fig.add_trace(go.Scatter(
        x=x1.date,
        y=x1['opposition'] + x1['sem'],
        mode='lines',
        name='Upper Bound',
        line=dict(color='rgba(0,0,0,0)'),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=x1.date,
        y=x1['opposition'] - x1['sem'],
        mode='lines',
        name='Lower Bound',
        line=dict(color='rgba(0,0,0,0)'),
        fill='tonexty',
        fillcolor=color,
        showlegend=False
    ))



fig.update_layout(
    font_family="Arial",
    font_color="black",
    title_font_family="Arial",
    title_font_color="black",
    title_font_size = 18,
    font_size = 16,
    title = '',
    legend_title_font_color="black", 
    template='presentation',
    yaxis_title="Opposition",
    yaxis_tickformat='2%',
    xaxis_title="",
    xaxis_tickformat='%b-%y',
    title_x=0.05, 
    showlegend=True,
    width=800,
    height=500,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=.35,
        font=dict(size=18, color="black", family=config.font),
    ), 
    legend_title_text='',
)

# reduce margins 
fig.update_layout(margin=dict(l=70, r=40, t=50, b=40, pad=1))
# make lines thicker
fig.update_traces(line=dict(width=4))


#fig.show()
fig.write_image("figure2.png")



# Figure 3: Effects of COVID-19 Infection on Opposition to COVID-19 Policies

### This figure uses the estimates from the matrix completion models in R. I have saved the estimates in a csv file, so you can directly use the data from the cell below.


# read data 
fig3 = pd.read_csv('figure3.csv')

#rename columns
fig3.columns = ['time', 'ATT', 'S.E.', 'lower_bound', 'upper_bound', 'pval', 'count']

# narrow the dataset to the time period of interest 
fig3=fig3.loc[(fig3.time <= 2)&(fig3.time > -2)]

# add a column 95% confidence interval
fig3['se'] = fig3['S.E.'] * 1.96

## create figure 
fig = go.Figure()


# assign colors 
color = config.colors[1]


# add the effect estimate and 95% confidence intervals to the plot
fig.add_trace(go.Scatter(line=dict(color=color),
                         x=fig3['time'],
                         y=fig3['ATT'],
                         name='Effect Estimate',
                         error_y=dict(type='data', array = fig3['se'], visible=True,color=color),
                         marker_size=10,marker_symbol='diamond', marker_line_width=1, marker_color=color, marker_line_color='black', mode='lines+markers',))
    

fig.update_layout(
    font_family="Arial",
    font_color="black",
    title_font_family="Arial",
    title_font_color="black",
    title_font_size = 18,
    font_size = 16,
    legend_title_font_color="black", 
    template='presentation',
    yaxis_title="Estimated Coefficient",
    xaxis_title="",
    title_x=0.05, 
    showlegend=True,
    width=700,
    height=600,
    
    )

## move legend to horizontal 
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=.25,
    font_size=16,
    ))


# add vertical and horizontal lines
fig.add_vline(x=.5, line_width=3, line_dash="dash", line_color="black", opacity=.8)
fig.add_hline(y=0, line_width=3, line_dash='dash', line_color='black', opacity=.8)


# change line width
fig.update_traces(line=dict(width=3.5),)


## add annotation in bottom right corner
fig.add_annotation(
    x=1.05,
    y=-.23,
    text="Matrix Completion Estimates and 95% confidence intervals",
    showarrow=False,
    xref="paper",
    yref="paper",
    font=dict(size=14, color="black", family=config.font),
    opacity=0.8,
)

# change margins and add in x axis title, remove zero lines (they're redundant)
fig.update_layout(margin=dict(l=70, r=70, t=50, b=110, pad=1), showlegend=False, 
                  xaxis_title='Time Relative to Infection',
                  xaxis=dict(zeroline=False, ),
                    yaxis=dict(zeroline=False, ),
                  )

# rename x axis ticks so that there's a tick for the infection date between 0 and 1 
fig.update_xaxes(ticktext=['-4 weeks', '-2 weeks', 'Infection', '+2 weeks', '+4 weeks'], tickvals=[-1, 0, .5, 1, 2])


fig.show()
# save figure
fig.write_image("figure3.png")



# Figure 4: Exit Effects of COVID-19 Infection on Opposition to COVID-19 Policies

### This figure uses the estimates from the matrix completion models in R. I have saved the estimates in a csv file, so you can directly use the data from the cell below.



# read data
fig4 = pd.read_csv('figure4.csv')

# rename columns
fig4.columns = ['time', 'ATT', 'S.E.', 'CI.lower', 'CI.upper', 'p.value','count']

# add a column 95% confidence interval
fig4['se'] = fig4['S.E.'] * 1.96


# narrow the dataset to the time period of interest
fig4 = fig4.loc[(fig4.time <= 7)&(fig4.time >= -1)]

# make tick values for the X axis (every estimate represents a 2 week period)
fig4['Time'] = (fig4.time + 2) * 2
fig4['Time'] = fig4['Time'].astype(str) + ' weeks'

# create figure
fig = go.Figure()


# assign colors
color = config.colors[1]


# add the effect estimate and 95% confidence intervals to the plot
fig.add_trace(go.Scatter(line=dict(color=color),
                         x=fig4['time'],
                         y=fig4['ATT'],
                         name='Effect Estimate',
                         error_y=dict(type='data', array = fig4['se'], visible=True,color=color),
                         marker_size=10,marker_symbol='diamond', marker_line_width=1, marker_color=color, marker_line_color='black', mode='lines+markers',))
    

fig.update_layout(
    font_family="Arial",
    font_color="black",
    title_font_family="Arial",
    title_font_color="black",
    title_font_size = 18,
    font_size = 16,
    legend_title_font_color="black", 
    template='presentation',
    yaxis_title="Estimated Coefficient",
    xaxis_title="",
    title_x=0.05, 
    showlegend=True,
    width=800,
    height=600,
    )

## move legend to horizontal 
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=.25,
    font_size=16,
    ))


#fig.add_vline(x=.5, line_width=3, line_dash="dash", line_color="black", opacity=.5)
fig.add_hline(y=0, line_width=3, line_dash='dash', line_color='black', opacity=.8)



#fig.update_traces(line=dict(width=.1))
fig.update_traces(line=dict(width=3.5),)


## add annotation in bottom right corner
fig.add_annotation(
    x=1.05,
    y=-.23,
    text="Matrix Completion Estimates and 95% confidence intervals",
    showarrow=False,
    xref="paper",
    yref="paper",
    font=dict(size=14, color="black", family=config.font),
    opacity=0.8,
)

fig.update_layout(margin=dict(l=70, r=70, t=50, b=110, pad=1), showlegend=False, 
                  xaxis_title='Time Relative to Infection',
                  xaxis=dict(zeroline=False, ),
                  yaxis=dict(zeroline=False, )
                  )

# rename x axis ticks
fig.update_xaxes(ticktext=fig4['Time'], tickvals=fig4['time'])


# make area while infected grey
fig.add_vrect(x0=-1.1, x1=0.1, fillcolor="lightgrey", opacity=0.5, line_width=0)


# add annotation for while infected
fig.add_annotation(
    x=.055,
    y=1,
    text="<b>Infection</b>",
    showarrow=False,
    xref="paper",
    yref="paper",
    font=dict(size=18, color="black", family=config.font),
    opacity=0.8,
)

fig.show()
# save figure
fig.write_image("figure4.png")



# Appendix Figure A1: Bert Model Evaluation

## calculate the F1 score for the predicted values and the hand coded 
from sklearn.metrics import f1_score # install scikit-learn if you don't have it installed

# read in the hand coded data
validate = pd.read_csv('validation_tweets.csv')


## loop through 10000 samples of 500 tweets and calculate the F1 score for each sample
lst = []

for i in range(10000):
    x = validate.sample(500)
    score = f1_score(x['annotated'], x['predicted'], average='weighted')
    lst.append(score)
    
    
# print F1 score from all data 
print('F1 Score:') 
print(f1_score(validate['annotated'], validate['predicted'], average='weighted'))


# create histogram of F1 scores

# assign colors
color = config.colors[1]

fig = px.histogram(pd.DataFrame(lst, columns=['F1 Score']), x='F1 Score', nbins=20, title='<b>F1 Score Distribution for Fine-Tuned Bert Model</b>', 
                   labels={'F1 Score':'F1 Score', 'count':'Count'},
                   color_discrete_sequence=[color], 
                   )

fig.update_layout(
    font_family="Arial",
    font_color="black",
    title_font_family="Arial",
    title_font_color="black",
    title_font_size = 18,
    font_size = 16,
    legend_title_font_color="black", 
    template='presentation',
    xaxis_title="",
    title_x=0.05, 
    showlegend=True,
    width=800,
    height=600,
    )
## add annotation in bottom right corner
fig.add_annotation(
    x=1.08,
    y=-.23,
    text="<b>Note:</b> F1 score using 10,000 samples of 500 from 1,000 annotated tweets the model had not seen",
    showarrow=False,
    xref="paper",
    yref="paper",
    font=dict(size=14, color="black", family=config.font),
    opacity=0.8,
)
fig.update_layout(margin=dict(l=70, r=70, t=50, b=110, pad=1), showlegend=False, 
                  )
fig.show()

# save figure
fig.write_image("figureA1.png")



# Table A1: Descriptive Statistics - Twitter Messages

### This table uses the primary analysis dataset for descriptive statistics of the total number of tweets and the number of opposition tweets every two-week period of the analysis. 



# read dataset 
df = pd.read_csv('analysis_data.csv')

# convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# rename columns for latex table
df.rename(columns={'opposition_tweet_count': 'Opposition Tweets', 'total_tweets': 'Total Tweets'}, inplace=True)

# agg the dataset by date and calculate the sum and mean of the opposition label and total tweets, save as latex table
tab = df.groupby('date').agg({'Opposition Tweets': ['sum', 'mean'],
                        'Total Tweets': ['sum', 'mean']}).round(3).reset_index().to_latex(index=False)

# write latex table to file tableA1.tex
with open('tableA1.tex', 'w') as tf:
     tf.write(tab)
     
     
     
# Figure A3: Effects of COVID-19 Infection on Opposition to COVID-19 Policies in Press Releases

### This figure presents the estimates from the matrix completion models in R for the press releases data. I have saved the estimates in a csv file, so you can directly use the data from the cell below.


# read data 
fig3 = pd.read_csv('figureA3.csv')

#rename columns
fig3.columns = ['time', 'ATT', 'S.E.', 'lower_bound', 'upper_bound', 'pval', 'count']

# narrow the dataset to the time period of interest 
fig3=fig3.loc[(fig3.time <= 2)&(fig3.time > -2)]

# add a column 95% confidence interval
fig3['se'] = fig3['S.E.'] * 1.96

## create figure 
fig = go.Figure()


# assign colors 
color = config.colors[1]


# add the effect estimate and 95% confidence intervals to the plot
fig.add_trace(go.Scatter(line=dict(color=color),
                         x=fig3['time'],
                         y=fig3['ATT'],
                         name='Effect Estimate',
                         error_y=dict(type='data', array = fig3['se'], visible=True,color=color),
                         marker_size=10,marker_symbol='diamond', marker_line_width=1, marker_color=color, marker_line_color='black', mode='lines+markers',))
    

fig.update_layout(
    font_family="Arial",
    font_color="black",
    title_font_family="Arial",
    title_font_color="black",
    title_font_size = 18,
    font_size = 16,
    legend_title_font_color="black", 
    template='presentation',
    yaxis_title="Estimated Coefficient",
    xaxis_title="",
    title_x=0.05, 
    showlegend=True,
    width=700,
    height=600,
    
    )

## move legend to horizontal 
fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=.25,
    font_size=16,
    ))


# add vertical and horizontal lines
fig.add_vline(x=.5, line_width=3, line_dash="dash", line_color="black", opacity=.8)
fig.add_hline(y=0, line_width=3, line_dash='dash', line_color='black', opacity=.8)


# change line width
fig.update_traces(line=dict(width=3.5),)


## add annotation in bottom right corner
fig.add_annotation(
    x=1.05,
    y=-.23,
    text="Matrix Completion Estimates and 95% confidence intervals",
    showarrow=False,
    xref="paper",
    yref="paper",
    font=dict(size=14, color="black", family=config.font),
    opacity=0.8,
)

# change margins and add in x axis title, remove zero lines (they're redundant)
fig.update_layout(margin=dict(l=70, r=70, t=50, b=110, pad=1), showlegend=False, 
                  xaxis_title='Time Relative to Infection',
                  xaxis=dict(zeroline=False, ),
                    yaxis=dict(zeroline=False, ),
                  )

# rename x axis ticks so that there's a tick for the infection date between 0 and 1 
fig.update_xaxes(ticktext=['-4 weeks', '-2 weeks', 'Infection', '+2 weeks', '+4 weeks'], tickvals=[-1, 0, .5, 1, 2])


fig.show()
# save figure
fig.write_image("figureA3.png")



# Descriptive Statistics - Press Releases

### This table uses the primary analysis dataset for descriptive statistics of the total number of press releases and the number of opposition press releases every two-week period of the analysis.


# read dataset 
df = pd.read_csv('analysis_data.csv')

# convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# rename columns for latex table
df.rename(columns={'press_releases_opposition_count': 'Opposition Press Releases', 'press_releases_total': 'Total Press Releases'}, inplace=True)

# agg the dataset by date and calculate the sum and mean of the opposition label and total tweets, save as latex table
tab = df.groupby('date').agg({'Opposition Press Releases': ['sum', 'mean'],
                        'Total Press Releases': ['sum', 'mean']}).round(3).reset_index().to_latex(index=False)

# write latex table to file tableA1.tex
with open('tableA6.tex', 'w') as tf:
     tf.write(tab)

