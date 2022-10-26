
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

# Testing reading in the meta-data dataset as a substitute for the large data files
meta_data = pandas.read_json(path_or_buf='meta-data.jsonl', lines = True)

# Filter meta_data to the ids seen in query_list:
data_list = meta_data[meta_data.DBRECORDID.isin(query_list)]





