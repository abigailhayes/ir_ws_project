import pandas
from collections import defaultdict
import math
from bm25 import bm25

'''doc = pandas.read_csv(filepath_or_buffer='output_narrow.csv')
for i in range(0, len(doc)):
    if str(doc['DBRECORDID'][i]) == 'M25160198':
        print(doc['qstr'][i])
        print(doc['ABSTRACT'][i])'''

doc2 = pandas.read_csv(filepath_or_buffer='PPTranslatedAbstract_Title.csv', converters={"Preprocessed_Abstract": lambda x: x.strip("[]").replace("'","").split(", ")})

query = pandas.read_csv(filepath_or_buffer='PPTranslatedQuery.csv', converters={"Preprocessing": lambda x: x.strip("[]").replace("'","").split(", "), "candidates": lambda x: x.strip("[]").replace("'","").split(", ")})

d = bm25(doc2, query)

for entry in d:
    list = d[entry]
    scores = [d[entry][i] for i in range(len(d[entry])) if d[entry][i][1] == -1000]
    if len(scores) > 10:
        print(entry)
