import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash import html
from dash import dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame
import os
import numpy as np


def init_jobs_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/jobs/',
    )

    # Load dataframe
    currectDir = os.getcwd()
    print(currectDir)
    df = pd.read_csv('./data/cleaned_data/final_merged_cleaned_df.csv')

    explodeby_State_df = df.assign(state=df['state'].str.split(',').explode('state'))
    #explodeby_State_df.to_csv('./data/cleaned_data/explode_state_df.csv')
    explodeby_skill_df = df.assign(skill=df['skill'].str.split(',').explode('skill'))
    #explodeby_skill_df.to_csv('./data/cleaned_data/explode_skill_df.csv')

    # Jobtitle distribution bar plot
    groupby_title_df = df.groupby('title').size().reset_index(name='amount')
    job_distribution_fig = px.bar(groupby_title_df, x="title", y="amount", color='title')

    # Jobopening choropleth figure
    groupby_state_us_job_opening_df = explodeby_State_df.groupby('state').size().reset_index(name='amount')
    us_wide_job_opening_index = groupby_state_us_job_opening_df.index[groupby_state_us_job_opening_df['state'] == 'US National'] 
    us_wide_job_opening_row = groupby_state_us_job_opening_df.loc[groupby_state_us_job_opening_df['state'] == 'US National']
    us_wide_job_opening_amount = us_wide_job_opening_row['amount'].item()
    groupby_state_us_job_opening_df = groupby_state_us_job_opening_df.drop(us_wide_job_opening_index)
    us_job_opening_fig = px.choropleth(groupby_state_us_job_opening_df,
                                       locations=groupby_state_us_job_opening_df['state'],    
                                       locationmode="USA-states",          
                                       color='amount',
                                       range_color=[0, groupby_state_us_job_opening_df['amount'].max()],                            
                                       scope="usa")

    # Job skill piechart
    job_skill_df = explodeby_skill_df[~explodeby_skill_df['skill'].isnull()]
    groupby_job_skill_df = job_skill_df.groupby('skill').size().reset_index(name='amount')
    groupby_job_skill_df = groupby_job_skill_df.sort_values(by=['amount'], ascending=True)
    groupby_job_skill_df['amount_pct'] = round(groupby_job_skill_df['amount'] / groupby_job_skill_df['amount'].sum(), 2)
    population_of_skillset_fig = px.pie(groupby_job_skill_df, values='amount_pct', names='skill')

    # Skills acorss 3 unique titles (barchart)
    job_skill_df['skill'] = pd.Categorical(job_skill_df['skill'], categories=job_skill_df['skill'].unique())
    groupby_title_skill_df = job_skill_df.groupby(['skill', 'title']).size().to_frame('amount').reset_index()
    groupby_title_skill_df = groupby_title_skill_df.sort_values(by=['skill', 'title'])
    #groupby_title_skill_df.to_csv('./data/cleaned_data/groupby_title_skill_df.csv')
    fig_y = groupby_title_skill_df.skill.unique() 
    title_skill_fig = go.Figure()
    title_skill_fig.add_trace(go.Bar(
        y= fig_y,
        x= groupby_title_skill_df.loc[groupby_title_skill_df.title == 'Data Analyst'].amount,
        name='Data Analyst',
        orientation='h',
        marker=dict(
            color='rgba(0, 0, 255, 0.6)',
            line=dict(color='rgba(0, 0, 255, 0.6)', width=1)
        )
    ))
    title_skill_fig.add_trace(go.Bar(
        y= fig_y,
        x= groupby_title_skill_df.loc[groupby_title_skill_df.title == 'Data Engineer'].amount,
        name='Data Engineer',
        orientation='h',
        marker=dict(
            color='rgba(255, 0, 0, 0.6)',
            line=dict(color='rgba(255, 0, 0, 0.6)', width=1)
            
        )
    ))
    title_skill_fig.add_trace(go.Bar(
        y= fig_y,
        x= groupby_title_skill_df.loc[groupby_title_skill_df.title == 'Data Scientist'].amount,
        name='Data Scientist',
        orientation='h',
        marker=dict(
            color='rgba(0, 255, 0, 0.6)',
            line=dict(color='rgba(0, 255, 0, 0.6)', width=1)
        )
    ))
    title_skill_fig.update_layout(
    autosize=False,
    width=1300,
    height=900,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ))
    #skillset_horizontal_bar_fig = px.bar(groupby_job_skill_df, x="amount", y="skill", orientation='h')

    # Job degree figures
    job_degree_df = df[~df['degree'].isnull()]
    groupby_degree_job_opening_df = job_degree_df.groupby(['title', 'degree']).size().reset_index(name='amount')
    title_degree_fig = px.bar(groupby_degree_job_opening_df, x = "title", y = "amount", color = "degree", title = "")

    # Average Yearly Salary across States
    # Filter down to rows that contain yearly salary in 'salary' column and save in 'ys' variable
    ys = df.loc[df['salary'].str.contains('a year', na=False)]
    ys.head(5)
    #Splitting salary ranges before the - and after the -, into different columns
    ys[['low_sal', 'high_sal']] = df['salary'].str.split('-', 1, expand=True)
    #Removing 'a year' from 'high_sal'
    ys['low_sal'] = ys['low_sal'].str.replace(r'a year', '')
    ys['high_sal'] = ys['high_sal'].str.replace(r'a year', '')
    #Removing $ from both columns
    ys['high_sal'] = ys['high_sal'].str.replace(r'$', '')
    ys['low_sal'] = ys['low_sal'].str.replace(r'$', '')
    #Removing , from both columns
    ys['high_sal'] = ys['high_sal'].str.replace(r',', '')
    ys['low_sal'] = ys['low_sal'].str.replace(r',', '')
    #Converting 'low_sal', 'high_sal' columns to numeric columns to average later on
    ys['low_sal'] = pd.to_numeric(ys['low_sal'])
    ys['high_sal'] = pd.to_numeric(ys['high_sal'])
    #Creating new 'Average Salary' column to input mean calculations
    ys['average_salary'] = ys[['low_sal','high_sal']].mean(axis=1) #if original salary wasn't a range, that value was copied into the average automatically
    ys1 = ys.groupby(['state']).aggregate(lambda x: ','.join(map(str, x))) #group by the state column in 'ys' df
    ys1 = ys1.drop('US National', 0)
    av_sal = ys1['average_salary'] #extracting just 'average_salary' into new variable av_sal
    av_sal = av_sal.str.split(',', expand=True) #splitting the string of salaries into separate columns; to calulate mean by each state
    av_sal = av_sal.apply(pd.to_numeric)
    av_sal['state_salary'] = av_sal.mean(axis=1) #computing mean across the columns into new column named 'state_salary'
    av_sal['state'] = av_sal.index #making state index into it's own column
    av_sal['state_salary'] = av_sal['state_salary'].round(decimals = 1) #rounding the averages
    av_sal_fig = px.choropleth(av_sal, locations='state', locationmode="USA-states", color='state_salary', scope="usa", title="Average Annual Salaries Across United States")
    av_sal_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    
    # splitting the location column into city and state
    ys[['location', 'others']] = ys['location'].str.split("+", 1, expand=True)
    regex = r'(?P<City>[^,]+)\s*,\s*(?P<State>[^\s]+)'
    df1 = ys['location'].str.extract(regex)
    df1

    # combining city and state column with the main dataframe
    df_row_reindex = pd.concat([ys, df1], axis=1)
    df_row_reindex.head(10)
    fig2 = px.scatter(df_row_reindex, x="title", y="average_salary", color="location"
                    , hover_data=['average_salary'])
    fig2.update_layout(
    autosize=False,
    width=1450,
    height=850,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ))

    # Yearly Salary Comapny
    ys['average_salary'] = ys[['low_sal', 'high_sal']].mean(axis=1)
    cpy_sal = px.bar(df_row_reindex, x="company", y="average_salary", color="average_salary")
    cpy_sal.update_layout(
    autosize=False,
    width=1450,
    height=850,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ))
    # Create Layout
    dash_app.layout = html.Div(children=[
        html.H1(children='Job Distribution Across Job Titles'),
        dcc.Graph(id='job-distribution-graph',figure=job_distribution_fig),
        html.H1(children='Job Openings Across United States'), 
        dcc.Graph(id='job-opening-graph',figure=us_job_opening_fig),
        html.Div("Among all the job openings, {0} of them are US-wide available. The above diagram displays job openings with specific state location.".format(us_wide_job_opening_amount),
                 style={'textAlign': 'center'}),
        html.H1("Skills in Demand Across Job Sites"),
        dcc.Graph(id='skillset-polulation-pie-graph',figure=population_of_skillset_fig),
        html.H1("Skills in Demand Distribution Across Job Titles "),
        dcc.Graph(id='skillset-horizontal-bar-graph',figure=title_skill_fig),
        html.H1("Required Degrees Across Job Titles"),
        dcc.Graph(id='title-degree-bar-graph',figure=title_degree_fig),
        html.H1("Average Yearly Salary across United States"),
        dcc.Graph(id='scatter',figure=av_sal_fig),
        html.H1("Average Yearly Salary across Companies"),
        dcc.Graph(id='bar',figure=cpy_sal),
        html.H1("Average Yearly Salary Distribution across Different Titles in Each City, State"),
        dcc.Graph(id='location',figure=fig2),
        ],
        id='dash-container'
    )

    return dash_app.server


