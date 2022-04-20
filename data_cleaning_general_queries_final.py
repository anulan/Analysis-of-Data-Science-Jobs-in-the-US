# -*- coding: utf-8 -*-
"""data_cleaning_general_queries_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1D6UXczU9gKyD7Bk8memaHKP_M0-108az
"""

import pandas as pd
from google.colab import drive
#drive.mount('drive')
fj_copied_path = '/content/flexjobs.csv' 
di_copied_path = '/content/dice.csv'
sh_copied_path = '/content/simplyhired.csv'
#fj_df = pd.read_csv(copied_path, index_col=0)

fj_df = pd.read_csv(fj_copied_path, index_col=0)
di_df = pd.read_csv(di_copied_path, index_col=0)
sh_df = pd.read_csv(sh_copied_path, index_col=0)

sh_df.duplicated()
sh_df.drop_duplicates(inplace=True)
di_df.drop_duplicates(inplace=True)
fj_df.drop_duplicates(inplace=True)

fj_df['state'] = fj_df['location'].str.findall(r"[A-Z]{2}")
fj_df['state'] = [','.join(map(str, l)) for l in fj_df['state']]
fj_df = fj_df[(fj_df['state'].str.len() != 0)]
fj_df['state'] = fj_df['state'].str.replace(',US', '')
fj_df['state'].replace('US', 'US National', inplace=True)
index = fj_df[(fj_df['state'] == 'QC') | (fj_df['state'] ==  'BC') | (fj_df['state'] == 'ON')| (fj_df['state'] == 'ON,AB')|(fj_df['state'] == 'ON,BC')].index
fj_df.drop(index, inplace=True)
index_on = fj_df.loc[fj_df['state'].str.contains('ON',case=True)].index
fj_df.drop(index_on, inplace=True)
fj_df['state'] = fj_df['state'].str.replace('ON,|,QC', '')
fj_df["state"] = fj_df["state"].str.split(",").map(set).str.join(",")

fj_df['state'].value_counts()
#pd.set_option("display.max_rows", None)

di_df['state'] = di_df['location'].str.findall(r"[A-Z]{2}")
di_df['state'] = [','.join(map(str, l)) for l in di_df['state']]

di_df['state'] = di_df['state'].str.replace(',US', '')
di_df['state'] = di_df['state'].str.replace('DI,SQ,', '')
di_df['state'] = di_df['state'].str.replace('IG,NW,', '')
di_df['state'] = di_df['state'].str.replace('OM,', '')
di_df['state'] = di_df['state'].str.replace('AD,NE,', '')
di_df['state'] = di_df['state'].str.replace('AD,NE,', '')  
di_df['state'] = di_df['state'].str.replace('LL,', '') 
di_df['state'] = di_df['state'].str.replace('SA,IC,', '') 
di_df['state'] = di_df['state'].str.replace('SA,IC,JB,SA,', '') 
di_df['state'] = di_df['state'].str.replace('SA,IC,', '') 
di_df['state'] = di_df['state'].str.replace('AT,ME,CS,', '') 
di_df['state'] = di_df['state'].str.replace('SA,IC,', '') 
di_df['state'] = di_df['state'].str.replace('SS,', '') 
di_df['state'] = di_df['state'].str.replace('DE,EG,IT,', '') 
di_df['state'] = di_df['state'].str.replace('JB,SA,', '') 
di_df['state'] = di_df['state'].str.replace('DI,SQ', '')
di_df['state'] = di_df['state'].str.replace('LL', '') 
di_df['state'] = di_df['state'].str.replace(',NJ', 'NJ') 
di_df = di_df[(di_df['state'].str.len() != 0)]

di_df = di_df.loc[di_df['state']!= 'KL']
di_df.state.value_counts()

sh_df['state'] = sh_df['location'].str.findall(r"[A-Z]{2}")
#sh_df['state'] = [','.join(map(str, l)) for l in di_df['state']]
sh_df = sh_df[sh_df['location'] != 'Remote']
sh_df = sh_df[~sh_df['location'].str.contains('Remote')]
sh_df['state'] = [','.join(map(str, l)) for l in sh_df['state']]

sh_df.loc[sh_df['location'].str.contains('California'), 'state'] = 'CA'
sh_df.loc[sh_df['location'].str.contains('New York'), 'state'] = 'NY'
sh_df.loc[sh_df['location'].str.contains('Michigan'), 'state'] = 'MI'
sh_df.loc[sh_df['location'].str.contains('Pennsylvania'), 'state'] = 'PA'
sh_df.loc[sh_df['location'].str.contains('North Carolina'), 'state'] = 'NC'
sh_df.loc[sh_df['location'].str.contains('Virginia'), 'state'] = 'VA'
sh_df.loc[sh_df['location'].str.contains('Georgia'), 'state'] = 'GA'
sh_df.loc[sh_df['location'].str.contains('Massachusetts'), 'state'] = 'MA'
sh_df.loc[sh_df['location'].str.contains('United States'), 'state'] = 'US National'
sh_df.loc[sh_df['location'].str.contains('Tennessee'), 'state'] = 'TN'
sh_df.loc[sh_df['location'].str.contains('Alabama'), 'state'] = 'AL'
sh_df.loc[sh_df['location'].str.contains('Colorado'), 'state'] = 'CO'
sh_df.loc[sh_df['location'].str.contains('Texas'), 'state'] = 'TX'
sh_df.loc[sh_df['location'].str.contains('Colorado'), 'state'] = 'CO'
sh_df.loc[sh_df['location'].str.contains('Illinois'), 'state'] = 'IL'
sh_df.loc[sh_df['location'].str.contains('Maryland'), 'state'] = 'MD'
sh_df.loc[sh_df['location'].str.contains('Minnesota'), 'state'] = 'MN'
sh_df.loc[sh_df['location'].str.contains('Missouri'), 'state'] = 'MO'
sh_df.loc[sh_df['location'].str.contains('Utah'), 'state'] = 'UT'
sh_df.loc[sh_df['location'].str.contains('Washington State'), 'state'] = 'WA'
sh_df.loc[sh_df['location'].str.contains('Connecticut'), 'state'] = 'CT'
sh_df.loc[sh_df['location'].str.contains('Indiana'), 'state'] = 'IN'

sh_df['state'] = sh_df['state'].str.replace('AF,', '')

"""##Merge Datasets"""

frames = [di_df, sh_df,fj_df]
df = pd.concat(frames)
ds = df[df.title.str.contains('data scientist|data science engineer', case=False)]
ds = ds[~ds.title.str.contains('data engineer|analyst|analytic|Data Science Analyst|Visualization|data engineer|Consultant|Senior Project Manager|Data Science Lead|Data Specialist',case=False)]
print(len(ds))

da = df[df.title.str.contains('Data Analyst|analyst|analytic|Data Science Analyst|Visualization', case=False)]
#analyst_overlap = analyst[analyst.title.str.contains('analytic|scientist', case=False)]
da = da[~da.title.str.contains('data scientist|data engineer|data scientist|data science engineer|Business Analyst|Data Specialist|database|scientist|Software Engineer|Consultant|Senior Project Manager|Data Science Lead|Data Specialist|Data Specialist', case=False)]
print(len(da))

de = df[df.title.str.contains('data engineer', case=False)]
de = de[~de.title.str.contains('data scientist|analyst|analytic|Data Science Analyst|Visualization|data science engineer|scientist|analyst|analytic|software engineer|AI Engineer', case=False)]
print(len(de))

print(len(ds) + len(da) + len(de))

title_ls = pd.concat([da.title, de.title, ds.title])
type(ds)
df = df.loc[(df.title.isin(title_ls))]
df.shape
df.loc[df.title.isin(ds.title), df.columns.difference(['salary', 'jobtype', 'location', 'description', 'company', 'state'])] = 'Data Scientist'
df.loc[df.title.isin(da.title), df.columns.difference(['salary', 'jobtype', 'location', 'description', 'company','state'])] = 'Data Analyst'
df.loc[df.title.isin(de.title), df.columns.difference(['salary', 'jobtype', 'location', 'description', 'company','state'])] = 'Data Engineer'
df.title.value_counts()

ds = df[df.title.str.contains('data scientist|data science engineer', case=False)]
ds = ds[~ds.title.str.contains('data engineer|analyst|analytic|Data Science Analyst|Visualization|data engineer|Consultant|Senior Project Manager|Data Science Lead|Data Specialist',case=False)]
print(len(ds))

da = df[df.title.str.contains('Data Analyst|analyst|analytic|Data Science Analyst|Visualization', case=False)]
da = da[~da.title.str.contains('data scientist|data engineer|data scientist|data science engineer|Business Analyst|Data Specialist|database|scientist|Software Engineer|Consultant|Senior Project Manager|Data Science Lead|Data Specialist|Data Specialist', case=False)]
print(len(da))

de = df[df.title.str.contains('data engineer', case=False)]
de = de[~de.title.str.contains('data scientist|analyst|analytic|Data Science Analyst|Visualization|data science engineer|scientist|analyst|analytic|software engineer|AI Engineer', case=False)]
print(len(de))

print(len(ds) + len(da) + len(de))

title_ls = pd.concat([da.title, de.title, ds.title])
type(ds)
df = df.loc[(df.title.isin(title_ls))]
df.shape
df.loc[df.title.isin(ds.title), df.columns.difference(['salary', 'jobtype', 'location', 'description', 'company','state'])] = 'Data Scientist'
df.loc[df.title.isin(da.title), df.columns.difference(['salary', 'jobtype', 'location', 'description', 'company','state'])] = 'Data Analyst'
df.loc[df.title.isin(de.title), df.columns.difference(['salary', 'jobtype', 'location', 'description', 'company','state'])] = 'Data Engineer'
df.title.value_counts()

df.reset_index(drop=True, inplace=True)

import re
df['description'] = df['description'].str.replace('machine learning|ml', 'ML', flags=re.I)
df['description'] = df['description'].str.replace('visualization|dashboard|tableau|Power BI', 'VISUALIZATION', flags=re.I)
df['description'] = df['description'].str.replace('python|python programming', 'PYTHON', flags=re.I)
df['description'] = df['description'].str.replace(' R |, R | /R/', ' R ', flags=re.I)
df['description'] = df['description'].str.replace('SQL|structured query language', 'SQL', flags=re.I)
df['description'] = df['description'].str.replace('Spark', 'SPARK', flags=re.I)
df['description'] = df['description'].str.replace('Hadoop|HDFS', 'HADOOP', flags=re.I)
df['description'] = df['description'].str.replace('statistic', 'STATISTICS', flags=re.I)

df['description'] = df['description'].str.replace('bachelor|undergraduate degree| BA | BS |B.S.|B.A.', ' BACHELOR ', flags=re.I)
df['description'] = df['description'].str.replace("masters degree|master degree|graduate degree| MS |or Master|masters|Masterâ€™s| Master's|MS/MA", ' MASTER ', flags=re.I)
df['description'] = df['description'].str.replace('phd|ph.d|doctorate', ' PHD ', flags=re.I)

skillsets = ['ML', 'VISUALIZATION', 'PYTHON', 'R', 'SQL', 'SPARK', 'HADOOP', 'STATISTICS']

df['skill'] = ''

for index, row in df.iterrows():
    skills = []
    descriptions = str(row['description']).split()

    for desc in descriptions:
        if desc.upper() in skillsets:
            skills.append(desc.upper())

    skills = list(set(skills))
    skills = [str(element) for element in skills]
    skillset = ''
    
    if len(skills) > 0:
         skillset = ','.join(skills)

    row['skill'] = skillset

df['description'] = df['description'].str.replace('bachelor|undergraduate degree| BA | BS |B.S.|B.A.', ' BACHELOR ', flags=re.I)
df['description'] = df['description'].str.replace("masters degree|master degree|graduate degree| MS |or Master|masters|Masterâ€™s| Master's|MS/MA", ' MASTER ', flags=re.I)
df['description'] = df['description'].str.replace('phd|ph.d|doctorate', ' PHD ', flags=re.I)

degree_ls = ['BACHELOR', 'MASTER', 'PHD']

df['degree'] = ''

for index, row in df.iterrows():
    degrees = []
    descriptions = str(row['description']).split()
  
    for desc in descriptions:
        if desc.upper() in degree_ls:
            degrees.append(desc.upper())
            
    degrees = list(set(degrees))
    degrees = [str(element) for element in degrees]
    degree = ''
    
    if len(degrees) > 0:
         degree = ','.join(degrees)

    row['degree'] = degree

df.loc[(df.degree.str.contains('phd',case=False)) & (df.title == 'Data Analyst')]

df.drop_duplicates(inplace=True)

df.to_csv('final_merged_cleaned_df_no_duplicate.csv')

"""## General Queries



"""

# Checking how many unique values the o categories in the dataset have
cat = df.select_dtypes(include = ['object'])
cat.apply(pd.Series.nunique)

#to check the distribution of the job types across the data set
df.groupby('title').count()
# we see that Data Analyst job and degrees fot it are more than the rest in count in the dataset.

df.isnull().sum()
# the 'company', 'salary' and 'jobtype' columns contain numerous null values

y = df.query("title == 'Data Scientist' and state== 'CA'")[['company']]
y
#locate companies of Data Science jobs in CA

df.groupby('title')['degree'].unique()
# No PHD degrees in Data Engineer jobs

group = df.groupby('state')
data_science_df = group.get_group('MI')
data_science_df.groupby(['title']).sum()

# MI seems to have less entries in these type of jobs