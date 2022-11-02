
# Loading packages:
import sys
import os
import pandas

# Changing working directory to the location of the current file:
os.chdir(os.path.dirname(sys.argv[0]))
print(os.getcwd())

# Read in 'candidates' data:
hq_can_train = pandas.read_json(path_or_buf='candidates/livivo_hq_100_candidates.jsonl', lines=True)
hq_can_train.rename(columns={'qid:': 'qid'}, inplace=True)
hq_train = pandas.read_json(path_or_buf='candidates/livivo_hq_1000.jsonl', lines=True)
hq_can_test = pandas.read_json(path_or_buf='candidates/livivo_hq_test_100_candidates.jsonl', lines=True)
hq_can_test.rename(columns={'qid:': 'qid'}, inplace=True)
hq_test = pandas.read_json(path_or_buf='candidates/livivo_hq_test_100.jsonl', lines=True)

# Testing reading in the meta-data dataset as a substitute for the large data files
meta_data = pandas.read_json(path_or_buf='meta-data.jsonl', lines = True)

# Obtaining all available abstracts relevant to each query
query = pandas.DataFrame(columns = ['qid', 'qstr', 'recordid', 'title', 'abstract'])
for i in range(len(hq_can_train)):
    query_list = hq_can_train.candidates[i]
    data_list = meta_data[meta_data.DBRECORDID.isin(query_list)]
    extra_data = hq_can_train.loc[[i]]
    new_data = data_list.merge(extra_data, how='cross')[['qid', 'qstr', 'DBRECORDID', 'TITLE', 'ABSTRACT']].rename(columns={'DBRECORDID': 'recordid', 'TITLE': 'title', 'ABSTRACT': 'abstract'})
    query = pandas.concat([query, new_data])
