
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

# Testing extracting data - using query 1 from the training candidate dataset
query_list = (hq_can_train[hq_can_train.qid.eq(1)])['candidates'][0]

# Testing reading in the meta-data dataset as an example - probably a faster way to do this
meta_data = pandas.read_json(path_or_buf='meta-data.jsonl', lines=True)
meta_data2 = dict()
for i in range(len(meta_data)):
    data_entry = dict(meta_data[0][i])
    meta_data2[data_entry["DBRECORDID"]] = data_entry
    
# Filter meta_data2 to the ids seen in query_list:
data_list = dict()
for i in range(len(query_list)):
    if query_list[i] in meta_data2:
        data_list[query_list[i]] = meta_data2[query_list[i]]
    else:
        continue



