

import os 
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='notebook'
import statsmodels.api as sm
from statsmodels.nonparametric.smoothers_lowess import lowess


# dictionary to map party names to respective colors
party_colors = {'Christian Democracy': '#1f77b4',
                'Conservative': '#9D755D',
                'Liberal': '#EECA3B',
                'Green': '#54A24B',
                'Radical Right-wing': '#222A2A',
                'Social Democracy': '#E45756',}






# function to clean the GLES data 
def clean_GLES_data(path):
    df = pd.read_stata(path, convert_categoricals=False)
    
    party_dict = {
        1: 'CDU/CSU',
        4: 'SPD',
        5: 'FDP',    
        6: 'Greens',
        7: 'DIE LINKE',
        322: 'AfD',
        801: 'other party'
    }

    climate_dict = {
        1: 'Pro-Climate Policy',
        2: 'Pro-Climate Policy',
        3: 'Pro-Climate Policy',
        5: 'Climate Policy Sceptic',
        6: 'Climate Policy Sceptic',
        7: 'Climate Policy Sceptic'
    }
    df['Climate Policy Preferences'] = df['kp15_1290'].map(climate_dict) 
    df['Party vote intention'] = df['kp15_190aa'].map(party_dict)

    df = df[['Climate Policy Preferences', 'Party vote intention']].dropna()
    
    return df 



def plot_figure_6(df, save=False, filename='figure6'):
    x = df.copy()   
    x = x.loc[x['Party vote intention'] != 'other party']
    ## map colors to official party colors 
    colors = x['Party vote intention'].map({
                  'other party': 'grey',
                  'CDU/CSU': 'blue',
                  'GRÜNE': 'green',
                    'SPD': 'red',
                    'FDP': 'yellow',
                    'DIE LINKE': 'purple',
                    'AfD': 'brown'})

    
    colors = x['Climate Policy Preferences'].map({'Climate Policy Sceptic':'#E45756', 'Pro-Climate Policy': '#54A24B'})
    
    fig = go.Figure(data=[go.Parcats(dimensions=[dict(values=x[f'Climate Policy Preferences'], label=f'Climate Policy Preferences'),
                                                    dict(values=x[f'Party vote intention'], label=f'Party Vote Choice')],
                                        line={'color': colors,}, 
                                         hoverinfo='count+probability',
                                         # add text labels to the end of each line
                                            labelfont={'size': 22, 'family': 'Arial', 'color': 'black'},
                                         # add space between boxes
                                            arrangement='perpendicular',)])
                                        
    

    fig.update_layout(width=900, height=500,
                      template = 'plotly_white',
                      margin = dict(l=140, r=130, b=75, t=60, pad=4),
                      font=dict(family="Arial", size=14, color="black"), 
                      title_font_size=24,
                      font_family="Arial",
                      xaxis_title = '',
                      font_color="black",
                      title_font_family="Arial",
                      title_font_color="black",
                      font_size = 18,
                      legend_title_font_color="black", 
                      )

            
    fig.update_coloraxes(showscale=False)
    
    
    #fig.update_traces(line_colorbar_xpad=100)
    fig.show(renderer="notebook")
    
    if save == True:
        try: 
            fig.write_image(f'../output/{filename}.png')
        except FileNotFoundError:
            os.mkdir('../output')
            fig.write_image(f'../output/{filename}.png')




## function to plot figure 5 
def plot_figure_5(df,
                    save=False,
                    save_filename=None):
    
    if save == True and save_filename == None:
        raise ValueError('Please specify a filename to save the plot')
    else:
        pass
    
    

    
    
    month = df[f'date'].dt.month.unique()[0]
    month_dic = ({1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'})
    year = df[f'date'].dt.year.unique()[0]
    
    date = f'{month_dic[month]}, {year}'
    
    #
    colors = df[f'Econ vs env. concerns (Wave 25)'].map({'Climate Policy Sceptic': '#E45756', 'Pro-Climate Policy': '#54A24B'})


    fig = go.Figure(data=[go.Parcats(dimensions=[{'values': df[f'Econ vs env. concerns (Wave 25)'], 'label': "Climate Policy Preferences"},
                                                    {'values': df[f'Party Vote (Wave 25)'], 'label': 'Party Vote Choice'}],
                                            line={'color': colors,}, 
                                            hoverinfo='count+probability',
                                                labelfont={'size': 22, 'family': 'Arial', 'color': 'black'},
                                                arrangement='perpendicular',),  

    ])
                                            
        

    fig.update_layout(width=900, height=500,
                        template = 'plotly_white',
                        #title = 'Climate Policy Skepticism and Party Vote Choice', 
                        margin = dict(l=140, r=190, b=45, t=60, pad=4),
                        font=dict(family="Arial", size=18, color="black"), 
                        title_font_size=34,
                        font_family="Arial",
                        xaxis_title = '',
                        font_color="black",
                        title_font_family="Arial",
                        title_font_color="black",
                        font_size = 20,
                        legend_title_font_color="black", 
                        )
                #plot_bgcolor='#c1c8d4',
                #paper_bgcolor='#c1c8d4'
                
    fig.update_coloraxes(showscale=False)
    fig.update_annotations(font_size=27, font_family='Arial', font_color='black')
    
    fig.show(renderer="notebook")
    
    if save == True:
        try: 
            fig.write_image(f'../output/{save_filename}.png')
        except FileNotFoundError:
            os.mkdir('../output')
            fig.write_image(f'../output/{save_filename}.png')
    



# function to clean BES data for figure 5 

def clean_BES_data_5(path):
    
    ## british data -- BES 

    df = pd.read_stata(path, convert_categoricals=False)

    ## map general election vote to parties 

    party_dict = {0: 'Would not vote', 1: 'Conservative', 2: 'Labour', 3: 'Liberal Democrat', 4: 'SNP', 5: 'Plaid Cymru', 6: 'Brexit Party/Reform UK', 7: 'Green Party', 8: 'Brexit Party/Reform UK', 11: 'Change UK', 12: 'Brexit Party/Reform UK', 13: 'Brexit Party/Reform UK/UKIP'}


    df[[i for i in df.columns if 'generalelectionvotew' in i.lower()]] = df[[i for i in df.columns if 'generalelectionvotew' in i.lower()]].apply(lambda x: x.map(party_dict))


    
    ## assign pro-growth and pro-environmental positions 
    def assign_env(df, var, min, max): 
        df['econ_env'] = np.nan
        df.loc[df[var].isin(list(range(0, min+1))), 'econ_env'] = 'Climate Policy Sceptic'
        df.loc[df[var].isin(list(range(max, 11))), 'econ_env'] = 'Pro-Climate Policy'
        #df = df.loc[df.econ_env.notna()]    
        return df['econ_env'].values


    for i in [i for i in df.columns if 'envirogrowthw' in i.lower()]:
        print(i)
        df[f'{i}_str'] = assign_env(df, i, 4, 6)
    
    df = df[[i for i in df.columns if 'envirogrowthw' in i.lower()]+[i for i in df.columns if 'generalelectionvotew' in i.lower()]+[i for i in df.columns if 'envirogrowthw' in i.lower()] + [i for i in df.columns if 'starttime' in i.lower()]]
    
    
    df = df[[f'enviroGrowthW25_str', f'generalElectionVoteW25', f'starttimeW25']].copy()
    
    df[f'generalElectionVoteW25'] = df[f'generalElectionVoteW25'].str.replace('Brexit Party/Reform UK', 'Reform UK/UKIP')
    
    # drop regional parties 
    df = df.loc[~df[f'generalElectionVoteW25'].isin(['Plaid Cymru', 'SNP', 'Would not vote'])].dropna()
    

    
    
    df = df[[f'enviroGrowthW25_str', f'generalElectionVoteW25', f'starttimeW25']].reset_index(drop=True)
    
    
    df.columns = ['x', f'Econ vs env. concerns (Wave 25)', f'Party Vote (Wave 25)', f'date']
    del df['x']
    
    return df 



# function to plot figure 7 

def plot_figure_7(df, 
                  save=True,
                  save_filename='figure7'): 

    if save == True and save_filename == None:
        raise ValueError('Please specify a filename to save the plot')
    else:
        pass
    
    fig = go.Figure()

    # Define dimensions
    dimensions = [
        dict(label="May 2020", values=df["May 2020"]),
        dict(label="May 2023", values=df["May 2023"])
    ]

    # Define color scale
    color_scale = [(0, '#54A24B'), (1, '#E45756')]

    # Add parallel categories trace
    fig.add_trace(go.Parcats(
        dimensions=dimensions,
        line=dict(color=df['climate'], colorscale=color_scale),
        hoveron='color',
        hoverinfo='count+probability',
        labelfont=dict(size=18, color='white')
    ))

    fig.update_layout(width=1000, height=700,
                        template = 'plotly_white',
                        #title = 'Climate Policy Skepticism and Party Vote Choice', 
                        margin = dict(l=200, r=190, b=45, t=50, pad=4),
                        font=dict(family="Arial", size=18, color="black"), 
                        title_font_size=34,
                        font_family="Arial",
                        xaxis_title = '',
                        font_color="black",
                        title_font_family="Arial",
                        title_font_color="black",
                        font_size = 20,
                        legend_title_font_color="black", 
                        showlegend = True,
                        )
                #plot_bgcolor='#c1c8d4',
                #paper_bgcolor='#c1c8d4'
                
    #fig.update_coloraxes(showscale=True)
    fig.update_annotations(font_size=27, font_family='Arial', font_color='black')

    # add legend 
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers+lines', name='Climate Policy Sceptic', marker=dict(color='#E45756'), showlegend=True))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers+lines', name='Pro Climate Policy', marker=dict(color='#54A24B'), showlegend=True))

    ## remove x axis ticks and labels
    fig.update_xaxes(showticklabels=False, showline = False, showgrid = False, zeroline = False)

    ## remove y axis ticks and labels
    fig.update_yaxes(showticklabels=False, showline = False, showgrid = False, zeroline = False)


    ## move legend to horizontal position
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-.1,
        xanchor="left",
        x=0.15, 
        itemwidth=30,
        #itemheight=30,
        itemsizing='constant',
        xref="paper",
        yref="paper",
        # make legend marker size larger
        
    ))


    ## add annotation below the legend 
    fig.add_annotation(
                x=-.05,
                y=1.05,
                text="<b>May 2020 (BES Wave 20)</b>",
                showarrow=False,
                font=dict(
                    family="Arial",
                    size=16,
                    color="black"
                ),
                xref="paper",
                yref="paper"
            )

    ## add annotation below the legend 
    fig.add_annotation(
                x=1.05,
                y=1.05,
                text="<b>May 2023 (BES Wave 25)</b>",
                showarrow=False,
                font=dict(
                    family="Arial",
                    size=16,
                    color="black"
                ),
                xref="paper",
                yref="paper"
            )


    # Show the plot
    fig.show()
    
    if save == True:
        try: 
            fig.write_image(f'../output/{save_filename}.png')
        except FileNotFoundError:
            os.mkdir('../output')
            fig.write_image(f'../output/{save_filename}.png')
    
    
    

# plot skepticism of Green policies using BES data 

def clean_BES_data_7(path):

    ## british data -- BES 
    df = pd.read_stata(path, convert_categoricals=False)

    ## map general election vote to parties 
    party_dict = {0: 'Would not vote', 1: 'Conservative', 2: 'Labour', 3: 'Liberal Democrat', 4: 'SNP', 5: 'Plaid Cymru', 6: 'Brexit Party/Reform UK', 7: 'Green Party', 8: 'Brexit Party/Reform UK', 11: 'Change UK', 12: 'Brexit Party/Reform UK', 13: 'Brexit Party/Reform UK/UKIP'}


    df[[i for i in df.columns if 'generalelectionvotew' in i.lower()]] = df[[i for i in df.columns if 'generalelectionvotew' in i.lower()]].apply(lambda x: x.map(party_dict))


    [i for i in df.columns if 'generalelectionvotew' in i.lower()]
    
    ## get responses for ids in waves 16, 17, 20, 23, 25
    all_climate = df.loc[(df.wave16 == 1)&(df.wave17 == 1)&(df.wave20 == 1)&(df.wave23 == 1)&(df.wave25 == 1)]
    
    # reduce the dataframe to only the relevant columns
    fig_df = all_climate[['enviroGrowthW16', 'enviroGrowthW17', 'enviroGrowthW20', 'enviroGrowthW23', 'enviroGrowthW25',
                      'generalElectionVoteW16', 'generalElectionVoteW17', 'generalElectionVoteW20', 'generalElectionVoteW23', 'generalElectionVoteW25']].dropna().reset_index()
    
    
    # wide to long 
    x = fig_df.melt(id_vars = ['index', 'generalElectionVoteW16', 'generalElectionVoteW17', 'generalElectionVoteW20', 'generalElectionVoteW23', 'generalElectionVoteW25'],
                value_vars = ['enviroGrowthW16', 'enviroGrowthW17', 'enviroGrowthW20', 'enviroGrowthW23', 'enviroGrowthW25'],
                var_name = 'wave', value_name = 'enviroGrowth')[['wave', 'enviroGrowth','index']]

    x1 = fig_df.melt(value_vars = ['generalElectionVoteW16', 'generalElectionVoteW17', 'generalElectionVoteW20', 'generalElectionVoteW23', 'generalElectionVoteW25'],
                id_vars = ['index', 'enviroGrowthW16', 'enviroGrowthW17', 'enviroGrowthW20', 'enviroGrowthW23', 'enviroGrowthW25'],
                var_name = 'wave', value_name = 'vote_choice')[['vote_choice']]

    df = pd.concat([x, x1], axis = 1)
    df['wave'] = df.wave.str.slice(-2, ).str.strip().astype(int)
    df = df.reset_index()
    df['entity'] = df['index']
    df['vote_cat'] = df['vote_choice'].astype('category')
    df.sort_values(['entity', 'wave'], inplace = True)


    del df['index'], df['level_0']

    df.reset_index(inplace = True, drop=True)
    df['lagged_econ_env'] = df.groupby('entity')['enviroGrowth'].shift(1)

    df['vote_cat'] = pd.Categorical(df.vote_cat).codes

    df.loc[df.vote_choice.isin(['Brexit Party/Reform UK/UKIP', 'UKIP', 'Reform UK']), 'RRW'] = 1
    df.RRW = df.RRW.fillna(0)

    df.loc[df.vote_choice == 'Reform UK', 'vote_choice'] = 'Brexit Party/Reform UK/UKIP'
    df.loc[df.vote_choice == 'UKIP', 'vote_choice'] = 'Brexit Party/Reform UK/UKIP'
    
    pcdf = fig_df.melt(id_vars = ['index', 'generalElectionVoteW16', 'generalElectionVoteW17', 'generalElectionVoteW20', 'generalElectionVoteW23', 'generalElectionVoteW25'],
            value_vars = ['enviroGrowthW16', 'enviroGrowthW17', 'enviroGrowthW20', 'enviroGrowthW23', 'enviroGrowthW25'],
            var_name = 'wave', value_name = 'enviroGrowth')
    
    ## create climate variable
    pcdf.loc[pcdf.enviroGrowth > 5, 'climate'] = 0
    pcdf.loc[pcdf.enviroGrowth < 5, 'climate'] = 1
    d = pcdf.loc[pcdf.climate != 'nan']
    
    
    # drop rows that contain party votes for anyone but Labour, Conservative, or Brexit Party/Reform UK
    cols = ['generalElectionVoteW16', 'generalElectionVoteW17', 'generalElectionVoteW20', 'generalElectionVoteW23', 'generalElectionVoteW25']
    parties = ['SNP','Would not vote', 'Change UK', 'Plaid Cymru', np.nan]
    d = d[~d[cols].isin(parties).any(axis=1)]
    
    
    d.loc[d.generalElectionVoteW25 == 'Brexit Party/Reform UK', 'generalElectionVoteW25'] = 'Brexit Party/Reform UK/UKIP'
    d.loc[d.generalElectionVoteW20 == 'Brexit Party/Reform UK', 'generalElectionVoteW20'] = 'Brexit Party/Reform UK/UKIP'

    d['May 2020'] = d.generalElectionVoteW20
    d['May 2023'] = d.generalElectionVoteW25
    d = d.loc[d.climate.notna()]
    
    # replace Brexit Party/Reform UK/UKIP with Reform UK/UKIP 

    d.loc[d['May 2020'] == 'Brexit Party/Reform UK/UKIP', 'May 2020'] = 'Reform UK/UKIP'
    d.loc[d['May 2023'] == 'Brexit Party/Reform UK/UKIP', 'May 2023'] = 'Reform UK/UKIP'
    
    return d 



# function to plot the proportion of party family voters who are skeptical of climate change

def plot_skepticism_by_family(outcome, 
                              save=False,
                              save_filename=None):
    
    if save == True and save_filename == None:
        raise ValueError('Please specify a filename to save the plot')
    else:
        pass
    
    ##### plot the proportions of each party family that are in favor of fossil fuel taxes
    if outcome == 'subsidize renewables':
        filepath = '../data/subsidise_renewables.csv'
    elif outcome == 'fossil fuel taxes':
        filepath = '../data/fossil_fuel_taxes.csv'
    else:
        raise ValueError('Please specify a valid outcome. Valid outcomes are "subsidize renewables" and "fossil fuel taxes"')

    x = pd.read_csv(filepath)

    ## plot the proportions of each party that are in favor of fossil fuel taxes
    x = x.loc[x.party_family != 'other/NA']
    #x = x.loc[x.party_family != 'other/NA']

    x.loc[x.party_family == 'Right-wing', 'party_family'] = 'Radical Right-wing'
    x.loc[x.party_family == 'Green/Ecologist', 'party_family'] = 'Green'
    x.loc[x.party_family == 'Social democracy', 'party_family'] = 'Social Democracy'
    x.loc[x.party_family == 'Christian democracy', 'party_family'] = 'Christian Democracy'




    fig = px.bar(x, x="party_family", y="normalized", color="position",title='', height=700, width=900, text_auto='0.000%', category_orders={'party_family': x.party_family.unique(), 'position': ['Against', 'Neither','Support']},
                color_discrete_sequence=['#E45756', 'lightgrey', '#54A24B'], text='normalized', barmode='stack', hover_data=['total'], template='plotly_white')



    fig.update_layout(
        legend=dict(
            title = 'Voter position'))

    fig.update_traces( textposition = "inside", textfont_size=20, textfont_color='black', textfont_family='Arial')
    fig.update_layout(xaxis = {"categoryorder":"total ascending"})

    fig.update_layout(
        font_family="Arial",
        font_color="black",
        title = '',
        title_font_family="Arial",
        title_font_size=24,
        title_font_color="black",
        font_size = 20,
        legend_title_font_color="black", 
        template='plotly_white',
        yaxis_title='',
        xaxis_title='',
        margin=dict(l=70, r=50, t=50, b=50),
        )

    fig.update_yaxes(tickformat=".0%", title_font_size=20, title_standoff=25, tickfont_size=16)

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=1.1,
        xanchor="right",
        x=.8,
        font = dict(size=20, color='black', family='Arial')
    ))

    fig.show(renderer="notebook")
    
    if save == True:
        try: 
            fig.write_image(f'../output/{save_filename}.png')
        except FileNotFoundError:
            os.mkdir('../output')
            fig.write_image(f'../output/{save_filename}.png')











# fucntion to plot the topic model heatmap 

def plot_topic_heatmap(filepath = '../data/topic_distributions.csv', ## specify the path to the topic distribution file
                       save=False,
                       save_filename=None):
    
    if save == True and save_filename == None:
        raise ValueError('Please specify a filename to save the plot')
    else:
        pass


    x=pd.read_csv(filepath)

    x['Topic'] = x['Unnamed: 0']

    del x['Unnamed: 0']

    x.set_index('Topic', inplace=True)

    fig = px.imshow(x, color_continuous_scale="algae", title = '<b>RRW press release topic distributions</b>', width=900,  height=800, aspect="auto", text_auto=True)

    fig.update_layout(
        font_family="Arial",
        font_color="black",
        title_font_family="Arial",
        title_font_size=26,
        title_font_color="black",
        font_size = 18,
        legend_title_font_color="black", 
        template='plotly_white',
        )


    fig.show(renderer="notebook")

    if save == True:
        try: 
            fig.write_image(f'../output/{save_filename}.png')
        except FileNotFoundError:
            os.mkdir('../output')
            fig.write_image(f'../output/{save_filename}.png')
            
            
            
            



def plot_country_subplots(df, 
                          frequency='Y',
                          save=False,
                          filename=None,
                          lowess_frac=0.14):
    
    if save == True and filename == None:
        raise ValueError('Please specify a filename to save the plot')
    else:
        pass

    x = df.groupby(['country', 'family_name', pd.Grouper(freq=frequency, key='date')]).agg({'environment': 'sum', 'climate_position': 'mean', 'environment_energy': 'sum', 'total': 'sum'}).reset_index()
    
    
    x = x.loc[~x.family_name.isin(['Agrarian', 'Special issue', 'Communist/Socialist'])]
    x['energy_env_proportion'] = x.environment_energy / x.total
    x['env_proportion'] = x.environment / x.total
    x['year'] = x.date.dt.year

    def map_to_3x3_pairs(number):
        if 1 <= number <= 9:
            row = (number - 1) // 3 + 1
            column = (number - 1) % 3 + 1
            return row, column
        else:
            return None


    ## make subplots for each country 
    from plotly.subplots import make_subplots

    fig = make_subplots(rows=3, cols=3, shared_yaxes = True,
                        vertical_spacing=.1, 
                        horizontal_spacing=.05, 
                        subplot_titles=('Austria', 'Denmark', 'Germany', 'Italy', 'Netherlands', 'Spain', 'Sweden', 'Switzerland', 'UK'))

    for row, country in enumerate(x.country.unique()):
        y = x[x.country == country]
        for family in y.family_name.unique():
            
            z = y[y.family_name == family]
            bp = pd.DataFrame({'year': pd.date_range('2010-01-01', '2023-01-01', freq='Y').year})
            z = pd.merge(bp, z, on='year', how='left')
            z.climate_position = z.climate_position.fillna(0)
            
            z['proportion_lowess'] = sm.nonparametric.lowess(z.climate_position, pd.Categorical(z.year).codes, frac=lowess_frac, it=0)[:, 1]
            fig.add_trace(go.Scatter(x=z.year, y=z.proportion_lowess, mode='markers+lines', name=family, showlegend=True if country == 'Netherlands' else False, line=dict(width=3, color=party_colors[family]), opacity=.7 if family != 'Radical Right-wing' else 1), row=map_to_3x3_pairs(row+1)[0], col=map_to_3x3_pairs(row+1)[1])


    ## make y axis ticks as percentages

    fig.update_yaxes(tickformat=".0%", title_font_size=20, title_standoff=25, tickfont_size=16)

    fig.update_layout(
        font_family="Arial",
        font_color="black",
        title_font_family="Arial",
        title_font_color="black",
        title_font_size = 12,
        font_size = 18,
        #yaxis_title='Proportion of press releases',
        legend_title_font_color="black", 
        template='presentation',
        title='',
        height=900, width=1000, 
        #plot_bgcolor='#c1c8d4',
        #paper_bgcolor='#c1c8d4',
        xaxis_title="",
        title_x=0.05, 
        showlegend=True,
        margin=dict(l=70, r=50, t=50, b=50)
        )

    fig.update_layout(legend=dict(
        title = 'Party Family',
        orientation="h",
        yanchor="bottom",
        y=-.25,
        xanchor="right",
        x=.9
    ))

    fig.update_annotations(font_size=20, font_family='Arial', font_color='black')

    fig.show(renderer="notebook")
    
    if save == True:
        try: 
            fig.write_image(f'../output/{filename}.png')
        except FileNotFoundError:
            os.mkdir('../output')
            fig.write_image(f'../output/{filename}.png')









## function to plot the second figure - party positions on climate change 

def plot_party_positions(df, 
                         filename=None,
                         save=False,
                         party_families = ['Christian Democracy', 'Conservative', 'Green',
                                   'Liberal', 'Social Democracy', 'Radical Right-wing'],
                         frequency='6M',
                         nuclear=True,
                         lowess_frac=0.14):
    """ 
    df: dataframe with party press releases
    frequency: frequency of the data, default is 6 months
    party_families: list of party families to include in the plot
    save: boolean, if True, the plot will be saved in the output folder
    nuclear: boolean, if True, the plot will include nuclear energy topics (default is False)
    """
    
    
    if save == True and filename == None:
        raise ValueError('Please specify a filename to save the plot')


    df['climate_position'] = df.climate_position.fillna(0).astype(float)
    x = df.loc[df.environment_energy == 1]

    ## change to get nuclear 
    if nuclear == False:
        x = x[~x.topic_model_topics.isin(['11_nuclear_expansion_power_plant', '1_nuclear_use_energy_environment'])]
    else: 
        pass 
    
    
    x = x.groupby(['family_name', pd.Grouper(key='date', freq=frequency)]).agg({'total': 'sum', 'climate_position': 'mean'}).reset_index()
    x = x.loc[x.family_name.isin(party_families)]


    fig = go.Figure()

    for family in party_families:
        y = x[x.family_name == family]
        y['proportion_lowess'] = sm.nonparametric.lowess(y.climate_position, pd.Categorical(y.date).codes, frac=lowess_frac, it=0)[:, 1]
        fig.add_trace(go.Scatter(x=y.date, y=y.proportion_lowess, mode='lines', name=family, line=dict(width=8, color=party_colors[family]), opacity=.7 if family != 'Radical Right-wing' else 1))

        
    fig.update_layout(
        font_family="Arial",
        font_color="black",
        title_font_family="Arial",
        title_font_color="black",
        title_font_size = 26,
        font_size = 18,
        yaxis_title='Policy Support',
        legend_title_font_color="black", 
        template='presentation',
        title='',
        height=600, width=950, 
        xaxis_title="",
        title_x=0.05, 
        showlegend=True,
        margin=dict(l=70, r=50, t=20, b=50)
        )

    fig.update_yaxes(tickformat=".0%", title_font_size=20, title_standoff=25, tickfont_size=16)

    fig.update_layout(legend=dict(
        title = 'Party Family',
        orientation="h",
        yanchor="bottom",
        y=-.25,
        xanchor="right",
        x=.9
    ))

    fig.show(renderer="notebook")
    
    
    
    if save == True:
        try: 
            fig.write_image(f'../output/{filename}.png')
        except FileNotFoundError:
            os.mkdir('../output')
            fig.write_image(f'../output/{filename}.png')






# function to display the first figure - issue salience over time 
def plot_issue_salience(df,
                        party_families = ['Christian Democracy', 'Conservative', 'Green',
                                   'Liberal', 'Social Democracy', 'Radical Right-wing'],
                        frequency='M',
                        save=False,
                        lowess_frac=0.14):
    x = df.groupby(['family_name', pd.Grouper(freq=frequency, key='date')]).agg({'environment': 'sum', 'environment_energy': 'sum', 'total': 'sum'}).reset_index()
    
    x = x.loc[x.family_name.isin(party_families)]
    
    
    x['energy_env_proportion'] = x.environment_energy / x.total
    x['env_proportion'] = x.environment / x.total


    fig = go.Figure()

    for family in party_families:
        y = x[x.family_name == family]
        y['proportion_lowess'] = sm.nonparametric.lowess(y.energy_env_proportion, pd.Categorical(y.date).codes, frac=lowess_frac, it=0)[:, 1]
        
        if family != 'Radical Right-wing':
            fig.add_trace(go.Scatter(x=y.date, y=y.proportion_lowess, mode='lines', name=family, line=dict(width=8, color=party_colors[family]), opacity=.7))
            
        else: 
            fig.add_trace(go.Scatter(x=y.date, y=y.proportion_lowess, mode='lines', name=family, line=dict(width=8, color=party_colors[family]), opacity=1))

    ## make y axis ticks as percentages

    fig.update_yaxes(tickformat=".0%", title_font_size=20, title_standoff=25, tickfont_size=16)

    fig.update_layout(
        font_family="Arial",
        font_color="black",
        title_font_family="Arial",
        title_font_color="black",
        title_font_size = 26,
        font_size = 18,
        yaxis_title='Proportion of press releases',
        legend_title_font_color="black", 
        template='presentation',
        title='',
        height=600, width=950, 
        xaxis_title="",
        title_x=0.05, 
        showlegend=True,
        margin=dict(l=70, r=50, t=20, b=50)
        )

    fig.update_layout(legend=dict(
        title = 'Party Family',
        orientation="h",
        yanchor="bottom",
        y=-.25,
        xanchor="right",
        x=.9
    ))

    fig.show(renderer="notebook")
    
    if save == True:
        try: 
            fig.write_image(f'../output/figure1.png')
        except FileNotFoundError:
            os.mkdir('../output')
            fig.write_image(f'../output/figure1.png')



def map_party_names(df):
    x = df.copy()
    x.groupby(['party_name', 'party_name_english']).agg({'total': 'sum'}).reset_index()
    x = dict(zip(x.party_name_english, x.party))
    x.update({'Alliance for the Future of Austria': 'BZÖ','New Right': 'NB', 'National Front': 'RN', 'Voice': 'VOX', 'Brothers of Italy': 'FdI', 'Forum for Democracy': 'FVD'})
    return x


def get_party_coverage(df):
    coverage = {}
    for party in df.party_name_english.unique():
        year_start = df[df.party_name_english == party].date.min().year
        year_end = df[df.party_name_english == party].date.max().year
        coverage[party] = f'{year_start}--{year_end}'
    return coverage


## group by country and party 
def get_all_party_descriptives(df):
    t = df.groupby(['country', 'party_name_english']).agg({'total': 'sum'}).reset_index()
    t['coverage'] = t.party_name_english.map(get_party_coverage(df))
    t['party_name'] = t.party_name_english.map(map_party_names(df))
    return print(t.to_latex(index=True))



def get_right_wing_descriptives(df, latex=False):
    x = df.copy()
    """
    df: dataframe with party press releases
    """
    x = x[x.family_name == 'Radical Right-wing']
    x = x.groupby(['country', 'party_name_english']).agg({'total': 'sum'}).reset_index()
    x['coverage'] = x.party_name_english.map(get_party_coverage(df))
    x['party_name'] = x.party_name_english.map(map_party_names(df))
    x = x[['country', 'party_name_english', 'party_name','coverage', 'total']]
    if latex == True:
        return print(x.to_latex(index=False))
    else:
        return x

