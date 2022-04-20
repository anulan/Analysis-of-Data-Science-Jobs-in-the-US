# Load data from the data folder

# Clean data

# Save data to the cleaned_data folder


import pandas as pd

df = pd.read_csv('./data/cleaned_data/merged_partially_cleaned_df.csv')
skillsets = ['ML', 'AL', 'VIS', 'PYTHON', 'R', 'SQL', 'SPARK', 'HADOOP', 'STATISTICS']

for index, row in df.iterrows():
    skills = []
    descriptions = str(row['description']).split()
    for desc in descriptions:
        if desc.upper in skillsets:
            skills.append(desc.upper)

    skillset = ','.join(map(str, skills))
    row['skill'] = skillset

print(df.head)

#df.to_csv('./data/cleaned_data/merged_partially_cleaned_skill_df.csv')
    
