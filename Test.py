import pandas as pd
import datetime
df = pd.read_csv("./OUTPUT-1/Restaurant.csv")
print(datetime.datetime(2021, 10, 17, 18, 52, 57, 782055))
print(df.head(5).describe)
print(len(df.ResId.unique()))
# 2021-10-18 02:39:36