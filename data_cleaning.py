import pandas as pd

df = pd.read_csv("job_offers.csv")

df = df.drop(columns="post_date")