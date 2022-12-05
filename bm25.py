import sys
import os
import pandas
from collections import defaultdict
import math


def get_term_weights(term: str, collection, N: int, array_entry:int) -> float:
    nt = 0
    for i in range(len(collection)):
        abstract = collection[i][array_entry]
        if term in abstract:
            nt += 1

    wt = 0.5*(N/nt)
    if wt < 0:
        print(nt)
    return wt


def bm25(doc, query):
    d = defaultdict()

    for j in range(len(query)):
        qid = query['qid:'][j]
        qstr = query['Preprocessing'][j]
        query_list = query['candidates'][j]
        abstracts = []
        for i in range(0, len(doc)):
            if doc['qid:'][i] != qid:
                continue
            if str(doc['DBRECORDID'][i]) in query_list:
                abstracts.append([doc["Preprocessed_Abstract"][i], doc['DBRECORDID'][i], doc["Preprocessed_Title"][i]])

        N = len(query_list)
        R = len(abstracts)
        sum = 0
        sum_titles = 0
        for abstract in abstracts:
            sum += len(abstract[0])
            sum_titles += len(abstract[2])
        lavg = sum / R
        lavg_title = sum_titles/N

        for i in range(R):
            abstract = abstracts[i][0]
            title = abstracts[i][2]
            score = -1000
            for term in qstr:
                if term in abstract:
                    wt = get_term_weights(term=term, collection=abstracts, N=N, array_entry=0)
                    ftd = abstract.count(term)
                    b = 0.75
                    k = 1
                    ld = len(abstract)
                    if score == -1000:
                        score = 0
                    score += (ftd * (k + 1)) / (ftd + k * (ld / lavg) * b + k * (1 - b)) * wt

                if term in title:
                    wt = get_term_weights(term=term, collection=abstracts, N=N, array_entry=2)
                    ftd = title.count(term)
                    b = 0.75
                    k = 1
                    ld = len(title)
                    if score == -1000:
                        score = 0
                    score += 0.05*(ftd * (k + 1)) / (ftd + k * (ld / lavg_title) * b + k * (1 - b)) * wt
            if qid in d.keys():
                d[qid][abstracts[i][1]] = score
            else:
                d[qid] = {abstracts[i][1]: score}

        for record_id in query_list:
            if record_id not in d[qid]:
                d[qid][record_id] = -1000

    '''for entry in d:
        d[entry] = sorted(d[entry].items(), key=lambda x: x[1], reverse=True)'''

    return d
