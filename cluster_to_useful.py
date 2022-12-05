# Modules needed
import pandas as pd


# Read in data
old_data = pd.read_csv("output/output_cluster.csv")

column_names = pd.DataFrame(old_data.columns.values, columns=["original"])
column_names["group"] = column_names["original"].str.replace("_.*", "")
column_unique = column_names["group"].unique().tolist()

for name in column_unique:
    col_names = column_names[column_names["group"]==name]["original"].tolist()
    v = old_data[col_names].values.tolist()
    old_data[(name+'_new')] = [[e for e in row if e==e] for row in v]
    
    
new_data = old_data.filter(regex='_new$',axis=1).iloc[: , 1:]
new_data.columns = new_data.columns.str.replace("_new", "") 

column_names2 = new_data.columns.values.tolist()
for name in column_names2:
    new_data[name] = new_data[name].str[0]

new_data.to_csv('output/output_narrow.csv')

