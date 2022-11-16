# Modules needed
import pandas

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

# Finding the relevent documents from each data file
for i, file_name in enumerate(name_data_files):
    new_data = pandas.read_json(path_or_buf=file_name, lines=True)
    query = query.merge(new_data, left_on='candidates', right_on='DBRECORDID', how='left')
    
# Saving the final file
query.to_json(path_or_buf='output.jsonl')
