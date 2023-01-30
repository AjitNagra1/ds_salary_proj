import pandas as pd
import numpy as np
import re

df = pd.read_csv("job_offers.csv")

# drop post_date column as not important
df = df.drop(columns="post_date")

# Change the name of the work_time column to salary_info 
df.rename(columns={"work_time":"salary_info"},inplace=True)

# replace values in the salary_info column with no salary info with the text "No salary info"
df["salary_info"] = np.where(~df["salary_info"].str.contains("0"), "No salary info", df["salary_info"])

# parse job descriptions for jobs which involve ML
df["machine_learning"] = df["job_desc"].apply(lambda x: 1 if ("machine learning" or "machine-learning") in x.lower() else 0)
# parse jobs which contain coding
df["coding"] = df["job_desc"].apply(lambda x: 1 if ("coding" or "programming" or "code" or "program" or "python" or "java" or "model") in x.lower() else 0)
# parse jobs which involve excel
df["excel"] = df["job_desc"].apply(lambda x: 1 if ("excel") in x.lower() else 0)

## cleaning and extracting the salary information from the salary_info column (assisted by ChatGPT)
def extract_salary(text):
    salary_pattern = re.compile(r'£(\d+,\d+)')
    salaries = re.findall(salary_pattern, text)
    return [int(salary.replace(',', '')) for salary in salaries]

df['salary_range'] = df['salary_info'].apply(extract_salary)

# drop the orginal salary_info column as now obselete
df = df.drop(columns="salary_info")

# Storing the data to csv file
df.to_csv('job_offers_cleaned.csv', index=False)







