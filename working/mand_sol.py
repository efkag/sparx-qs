import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# paths variables that we can later make into arguments etc
data_dir = "task_data"
csv_path = os.path.join(data_dir, "task_qla_df.csv") 
feather_path = os.path.join(data_dir, "task_tia_df.feather")

# read the files using pandas
qla_df = pd.read_csv(csv_path)
tia_df = pd.read_feather(feather_path)
print(qla_df)


# Q1
# Inner join and look for unique id numbers
merged = pd.merge(qla_df, tia_df, how='inner', on='student_id')['student_id']
uniq_students = merged.nunique('student_id')
print(uniq_students)

#Q2
# count assessments
assess_thresh = 2
#drop Nan mark values 
qla_clean = qla_df.dropna(axis=0, subset='mark')
grouped = qla_clean.groupby(['student_id'])['assessment_id'].count().reset_index()
students = grouped[grouped['assessment_id'] >= assess_thresh]['student_id']

# keep only the students who have >= 2 assessments
merged = pd.merge(students, qla_clean, how='inner', on='student_id')

# group by and calculate the mark diff within each group.
#TODO: for some reason it always produces NaNs as a resuls no matter what I tried
merged['progress'] = merged.groupby(['student_id'])['mark'].diff()
merged = merged.dropna()
print(merged)


#Q3
merged.hist(column='progress')
plt.show()

