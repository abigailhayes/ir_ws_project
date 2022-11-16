# Modules needed
import pandas
import json
import numpy as np

# File names
name_queries = ['livivo_hq_test_100_candidates.jsonl']
name_data_files = ['livivo_agris.jsonl',
                       'livivo_medline_00.jsonl',
                       'livivo_medline_01.jsonl',
                       'livivo_medline_02.jsonl',
                       'livivo_medline_03.jsonl',
                       'livivo_medline_04.jsonl',
                       'livivo_medline_05.jsonl',
                       'livivo_medline_06.jsonl',
                       'livivo_medline_07.jsonl',
                       'livivo_medline_08.jsonl',
                       'livivo_medline_09.jsonl',
                       'livivo_medline_10.jsonl',
                       'livivo_nlm.jsonl']

# Setting up desired documents for each query
queries = pandas.read_json(path_or_buf='livivo_hq_test_100_candidates.jsonl', lines=True)
query = queries.explode('candidates')
query[['abstract','title', 'keywords']] = np.nan
id_values = query["candidates"]

# Finding the relevent documents from each data file
for i, file_name in enumerate(name_data_files):
    with open(file_name, "rb") as f:
        for line in f:
            record = json.loads(line)
            if record["DBRECORDID"] in id_values.values:
                if "ABSTRACT" in record:
                    query.loc[query['candidates'] == record["DBRECORDID"], 'abstract']=[record["ABSTRACT"]]
                if "TITLE" in record:
                    query.loc[query['candidates'] == record["DBRECORDID"], 'title']=[[record["TITLE"]]]
                if "KEYWORDS" in record:
                    query.loc[query['candidates'] == record["DBRECORDID"], 'keywords']=[record["KEYWORDS"]]
    
# Saving the final file
query.to_csv(path_or_buf='output.csv')
