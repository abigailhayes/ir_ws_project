from collections import defaultdict

def baseline(doc, query):
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
                abstracts.append([doc["Preprocessed_Abstract"][i], doc['DBRECORDID'][i]])

        R = len(abstracts)

        for i in range(R):
            abstract = abstracts[i][0]
            score = -1000
            for term in qstr:
                if term in abstract:
                    ftd = abstract.count(term)
                    if score == -1000:
                        score = 0
                    score += ftd

            if qid in d.keys():
                d[qid][abstracts[i][1]] = score
            else:
                d[qid] = {abstracts[i][1]: score}

        for record_id in query_list:
            if record_id not in d[qid]:
                d[qid][record_id] = -1000

    return d
