
# Loading packages:
import sys
import os
import pandas

# Changing working directory to the location of the current file:
os.chdir(os.path.dirname(sys.argv[0]))
print(os.getcwd())

# Read in 'candidates' data:
hq_can = pandas.read_json(path_or_buf='candidates/livivo_hq_100_candidates.jsonl', lines=True)
hq = pandas.read_json(path_or_buf='candidates/livivo_hq_1000.jsonl', lines=True)
hq_can_test = pandas.read_json(path_or_buf='candidates/livivo_hq_test_100_candidates.jsonl', lines=True)
hq_test = pandas.read_json(path_or_buf='candidates/livivo_hq_test_100.jsonl', lines=True)
