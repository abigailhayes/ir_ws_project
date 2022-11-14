# Modules needed
import pandas

# File names
name_queries = list('livivo_hq_test_100_candidates.jsonl')
name_data_files = list('livivo_agris.jsonl',
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
                       'livivo_nlm.jsonl')

# Reading in data
queries = pandas.read_json(path_or_buf='livivo_hq_test_100_candidates.jsonl', lines=True)
data_files = pandas.read_json(path_or_buf=name_data_files[0], lines=True)
for i in range(1,len(name_data_files)):
    new_data_files = pandas.read_json(path_or_buf=name_data_files[i], lines=True)
    data_files = pandas.concat(data_files, new_data_files)
    
# Obtaining all available abstracts relevant to each query
query = pandas.DataFrame(columns = ['qid', 'qstr', 'recordid', 'title', 'abstract'])
for i in range(len(queries)):
    query_list = queries.candidates[i]
    data_list = data_files[data_files.DBRECORDID.isin(query_list)]
    extra_data = queries.loc[[i]]
    new_data = data_list.merge(extra_data, how='cross')[['qid', 'qstr', 'DBRECORDID', 'TITLE', 'ABSTRACT']].rename(columns={'DBRECORDID': 'recordid', 'TITLE': 'title', 'ABSTRACT': 'abstract'})
    query = pandas.concat([query, new_data])